"""원본 보존, 검증 누락, 경로 경계를 실제 임시 파일로 확인합니다."""

import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROUND = Path(__file__).resolve().parents[1]
SCRIPT = ROUND / "tools" / "dmf_air_quality.py"
DMF_ROOT = ROUND.parents[0] / "work" / "DMF"
APP = None
if SCRIPT.is_file():
    SPEC = importlib.util.spec_from_file_location("ict_dmf_adapter", SCRIPT)
    APP = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = APP
    SPEC.loader.exec_module(APP)


class AdapterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="ict-dmf-tests-")
        cls.base = Path(cls.temp.name)
        if APP is None:
            return
        cls.api = APP.load_dmf(DMF_ROOT)
        cls.source = cls.base / "원본"
        cls.source.mkdir()
        csv_bytes = (
            "timestamp,dht_temp_C,dht_humi_pct,am_temp_C,am_humi_pct,co2_ppm,voc_level,pm25_ugm3\r\n"
            "2026-10-03 00:00:00,20.4,50.0,21.0,50.0,799,1,15\r\n"
            "2026-10-03 00:00:02,,,30.0,81.0,1500,3,76\r\n"
        ).encode("utf-8")
        contents = [b"// Arduino fixture\r\n", b"print('fixture')\r\n", csv_bytes]
        cls.specs = []
        for spec, data in zip(APP.SOURCE_SPECS, contents):
            item = {**spec, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            path = cls.source / item["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            cls.specs.append(item)
        cls.prepared = cls.base / "기준결과"
        APP.build_bundle(cls.source, cls.prepared, cls.api, cls.specs)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.assertIsNotNone(APP, "원본 보존·검증 프로그램이 아직 구현되지 않았습니다")
        self.case = Path(tempfile.mkdtemp(dir=self.base))
        self.output = self.case / "결과"
        shutil.copytree(self.prepared, self.output)

    def verify(self):
        return APP.verify_bundle(self.source, self.output, self.api, self.specs)

    def mutate(self, name, fn):
        path = self.output / name
        value = json.loads(path.read_text(encoding="utf-8"))
        fn(value)
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def test_real_round_trip_and_readonly_verify(self):
        before = {p.relative_to(self.output).as_posix(): p.read_bytes()
                  for p in self.output.rglob("*") if p.is_file()}
        result = self.verify()
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["source_file_count"], 3)
        self.assertEqual(result["version_count"], 2)
        self.assertEqual(result["audit_count"], 2)
        after = {p.relative_to(self.output).as_posix(): p.read_bytes()
                 for p in self.output.rglob("*") if p.is_file()}
        self.assertEqual(after, before)

    def test_snapshot_keeps_crlf_bytes(self):
        for spec in self.specs:
            self.assertEqual((self.output / "원본보존" / spec["path"]).read_bytes(),
                             (self.source / spec["path"]).read_bytes())

    def test_snapshot_one_byte_change_is_rejected(self):
        path = self.output / "원본보존" / self.specs[0]["path"]
        path.write_bytes(path.read_bytes() + b"x")
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_sealed_digest_change_is_rejected(self):
        self.mutate("봉인_목록.json", lambda x: x["sources"][0].update(sha256="f" * 64))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_stored_manifest_root_change_is_rejected(self):
        self.mutate("버전_이력.json", lambda x: x["versions"][0].update(manifest_root="f" * 64))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_stored_restrict_seal_change_is_rejected(self):
        self.mutate("버전_이력.json", lambda x: x["versions"][0].update(restrict_seal="f" * 64))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_metadata_change_is_rejected(self):
        self.mutate("버전_이력.json", lambda x: x["versions"][1]["metadata"].update(title="변경"))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_document_identity_change_is_rejected(self):
        self.mutate("버전_이력.json", lambda x: x["versions"][1].update(document_id="다른문서"))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_nonconsecutive_version_is_rejected(self):
        self.mutate("버전_이력.json", lambda x: x["versions"][1].update(version_no=77))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_boolean_version_number_is_rejected_after_inventory_rehash(self):
        self.mutate("버전_이력.json", lambda x: x["versions"][0].update(version_no=True))
        changed = self.output / "버전_이력.json"
        def rehash(value):
            for item in value["files"]:
                if item["path"] == "버전_이력.json":
                    data = changed.read_bytes()
                    item.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        self.mutate("파일_무결성.json", rehash)
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_empty_audit_is_rejected(self):
        self.mutate("감사_이력.json", lambda x: x.update(entries=[]))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_audit_truncation_is_rejected(self):
        self.mutate("감사_이력.json", lambda x: x["entries"].pop())
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_audit_content_change_is_rejected(self):
        self.mutate("감사_이력.json", lambda x: x["entries"][0].update(actor="다른행위자"))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_audit_hash_failure_has_explicit_validation_error(self):
        self.mutate("감사_이력.json", lambda x: x["entries"][0].update(entry_hash="f" * 64))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_module_proof_change_is_rejected(self):
        self.mutate("모듈_증명.json", lambda x: x["proofs"][0].update(index=99))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_analysis_value_change_is_rejected(self):
        self.mutate("분석_결과.json", lambda x: x.update(valid_rows=999))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_report_text_change_is_rejected(self):
        path = self.output / "DMF_적용보고서.html"
        path.write_bytes(path.read_bytes() + b"changed")
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_missing_inventory_entry_is_rejected(self):
        self.mutate("파일_무결성.json", lambda x: x["files"].pop())
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_path_escape_is_rejected(self):
        for relative in ("../외부", "nested/../../외부", "/외부", "C:/외부", "a\\..\\외부"):
            with self.subTest(relative=relative), self.assertRaises(APP.ValidationError):
                APP.safe_child(self.output, relative)

    def test_output_inside_source_is_rejected(self):
        with self.assertRaises(APP.ValidationError):
            APP.build_bundle(self.source, self.source / "결과", self.api, self.specs)

    def test_existing_output_is_not_overwritten(self):
        before = (self.output / "봉인_목록.json").read_bytes()
        with self.assertRaises(APP.ValidationError):
            APP.build_bundle(self.source, self.output, self.api, self.specs)
        self.assertEqual((self.output / "봉인_목록.json").read_bytes(), before)

    def test_source_symlink_is_rejected(self):
        link = self.case / "원본링크"
        try:
            os.symlink(self.source, link, target_is_directory=True)
        except OSError as exc:
            self.skipTest("임시 symlink 생성이 지원되지 않습니다: " + str(exc))
        with self.assertRaises(APP.ValidationError):
            APP.build_bundle(link, self.case / "새결과", self.api, self.specs)

    def test_nested_snapshot_symlink_is_rejected(self):
        path = self.output / "원본보존" / self.specs[0]["path"]
        path.unlink()
        try:
            os.symlink(self.source / self.specs[0]["path"], path)
        except OSError as exc:
            self.skipTest("임시 symlink 생성이 지원되지 않습니다: " + str(exc))
        with self.assertRaises(APP.ValidationError):
            self.verify()

    def test_csv_statistics_match_hand_checked_rows(self):
        stats = APP.analyze_csv(self.source / self.specs[2]["path"])
        self.assertEqual(stats["total_rows"], 2)
        self.assertEqual(stats["valid_rows"], 2)
        self.assertEqual(stats["invalid_rows"], 0)
        self.assertEqual(stats["metrics"]["dht_temp_C"]["blank"], 1)
        self.assertEqual(stats["metrics"]["co2_ppm"]["max"], "1500")
        self.assertEqual(stats["code_level_counts"], [1, 0, 0, 1])
        self.assertEqual(stats["gaps_over_one_second"], 1)

    def test_csv_invalid_values_are_counted_without_rewriting(self):
        path = self.case / "비정상.csv"
        data = ("timestamp,dht_temp_C,dht_humi_pct,am_temp_C,am_humi_pct,co2_ppm,voc_level,pm25_ugm3\n"
                "2026-10-03 00:00:00,nan,50,21,50,800,0,7\n"
                "2026-10-03 00:00:01,,,,,,,\n"
                "잘못된시간,20,50,21,50,800,0,7\n"
                "2026-10-03 00:00:03,20,50\n")
        path.write_text(data, encoding="utf-8")
        stats = APP.analyze_csv(path)
        self.assertEqual(stats["invalid_rows"], 4)
        self.assertEqual(stats["valid_rows"], 0)
        self.assertEqual(stats["invalid_reasons"], {"nonfinite": 1, "all_blank": 1,
                                                  "timestamp": 1, "columns": 1})
        self.assertEqual(path.read_text(encoding="utf-8"), data)

    def test_csv_wrong_header_is_rejected(self):
        path = self.case / "다른열.csv"
        path.write_text("timestamp,value\n", encoding="utf-8")
        with self.assertRaises(APP.ValidationError):
            APP.analyze_csv(path)

    def test_wrong_dependency_commit_is_rejected(self):
        checkout = self.case / "의존성"
        git = shutil.which("git")
        subprocess.run([git, "clone", "--shared", "--no-checkout", str(DMF_ROOT), str(checkout)],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        tree = subprocess.run([git, "-C", str(checkout), "rev-parse", "HEAD^{tree}"],
                              check=True, capture_output=True, timeout=10).stdout.decode("ascii").strip()
        # 얕은 체크아웃에서도 부모 커밋 없이 격리된 다른 유효 커밋을 만듭니다.
        commit = subprocess.run([git, "-C", str(checkout), "-c", "user.name=격리검사",
                                 "-c", "user.email=test@example.invalid", "commit-tree", tree, "-m", "격리 검사 커밋"],
                                check=True, capture_output=True, timeout=10).stdout.decode("ascii").strip()
        subprocess.run([git, "-C", str(checkout), "update-ref", "HEAD", commit],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        with self.assertRaises(APP.ValidationError):
            APP.load_dmf(checkout)

    def test_cli_help_runs_without_hardware(self):
        run = subprocess.run([sys.executable, "-B", "-X", "utf8", str(SCRIPT), "--help"],
                             capture_output=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stderr.decode("utf-8", "replace"))

    def test_checked_python_and_korean_text_are_strict_utf8(self):
        for path in (SCRIPT, Path(__file__)):
            text = path.read_bytes().decode("utf-8", errors="strict")
            self.assertNotIn("\ufffd", text)
            ast.parse(text, filename=str(path))


if __name__ == "__main__":
    unittest.main()
