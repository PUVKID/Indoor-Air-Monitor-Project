"""수업의 공기질 원본을 보존하고 DMF로 로컬 무결성 증거를 생성·검증합니다."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import html
import json
import ntpath
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from types import ModuleType, SimpleNamespace


DMF_COMMIT = "cf550e3b2ceb0946ba89f64e43b7d6c2f5164383"
DMF_URL = "https://github.com/leecursion/DMF"
DOCUMENT_ID = "ict-safety-air-quality"
SOURCE_SPECS = [
    {"module_id": "source.arduino", "path": "아두이노 코드/dht_am1008w_lcd_csv/dht_am1008w_lcd_csv.ino",
     "bytes": 6894, "sha256": "02f2d255b51b88ac0a281aa07fd02f084617e0a25bfb6cb92119683dd536223a"},
    {"module_id": "source.logger", "path": "CSV 파이썬 코드/pc_csv_logger.py",
     "bytes": 2265, "sha256": "dfa31ebcbd9c9cac22ded7ebf55585364af4b969873891c12eec8bac09358dbd"},
    {"module_id": "source.measurements", "path": "CSV 파이썬 코드/air_log.csv",
     "bytes": 34551203, "sha256": "3e3584574c83d8fe56a69d263862194f5dab620308e8b133d00eb14b4be40bcc"},
]
DMF_BLOBS = {
    "__init__.py": "9f383ae996c4d37485614d01f9239198447c97d9cb1382ea418ad58cfb5bed8b",
    "canonical.py": "1be37bc188623f77ca59b151c616c86ca3276bbe3d0b285f5fb70c036da4bf7b",
    "merkle.py": "185d642ce155ccddb90d62c7c7e70e160cdc25777681d911cf66780c31d4dbfc",
    "manifest.py": "6f57102d1007640421eaf79c02999bdc2df161255af8e9d1c5c5c8368fb60eb2",
    "restrict.py": "ec651adc0a95acbb41f4a2d70378b600ccd199261dcdf3e1cfdef2a9721d078a",
    "merge.py": "6ddac1c17581c00882ece0442c1c3b3518f9bc24fad7b4312ba081b4b1224d7f",
    "audit_chain.py": "fdd4fbc42233e69c4fe2e5462c5cc05c2fb808e873aa3d3b32127b6e722aafc2",
}
FIELDS = ["dht_temp_C", "dht_humi_pct", "am_temp_C", "am_humi_pct", "co2_ppm", "voc_level", "pm25_ugm3"]
LABELS = ["DHT 온도", "DHT 상대습도", "AM 온도", "AM 상대습도", "CO₂", "VOC 단계", "PM2.5"]
UNITS = ["°C", "%", "°C", "%", "ppm", "센서 단계", "µg/m³"]
POLICY = {
    "t": "ict.dmf.processing-policy/v1", "header": ["timestamp"] + FIELDS,
    "numeric": "유한 Decimal만 분석하며 원문 바이트는 변환하지 않음",
    "timestamp": "PC 로컬 시각 문자열, 시간대 미기록, UTC로 환산하지 않음",
    "blank": "일부 결측은 보존, 모든 센서 결측은 분석 제외",
    "invalid": "원본 행은 보존하고 제외 사유별로 집계",
    "level": "원본 Arduino 판정 순서를 재현한 프로젝트 등급이며 공식 건강 기준이 아님",
    "originals": "고정 SHA-256과 크기로 최초 원본을 고정, 임의 재봉인 없음",
}
LIMITATIONS = [
    "실제 센서 재측정·장치 업로드·보정 정확도를 검사한 결과가 아닙니다.",
    "CSV 시각에는 시간대가 없으며 기록 범위가 연속 측정을 뜻하지 않습니다.",
    "프로젝트 LED 등급을 재현했으며 공인 안전·의료 판정을 수행하지 않습니다.",
    "DMF 서버·API·승인·권한·Shadow/Official 승격은 구현하지 않았습니다.",
    "외부 서명·타임스탬프·WORM이 없어 증거 전체를 다시 작성할 수 있는 주체까지 탐지하지 못합니다.",
    "DMF 라이선스가 확인되지 않아 외부 소스를 동봉하지 않고 별도 체크아웃을 사용합니다.",
]
CHECKS = ["고정 의존성 커밋·원문 해시", "원본 3파일 크기·SHA-256", "원본·스냅샷 바이트 일치",
          "처리 규칙 봉인", "CSV 재분석 대조", "동일 문서·연속 버전", "manifest·seal·version 재계산",
          "Restrict·위험도", "모듈 포함 증명", "감사 개수·연결·고정 head", "보고서·검증 JSON 일치",
          "도구 생성 파일 전체 크기·SHA-256"]
JSON_NAMES = ["봉인_목록.json", "처리_규칙.json", "분석_결과.json", "버전_이력.json", "감사_이력.json", "모듈_증명.json"]
REPORT_NAMES = ["검증_결과.json", "DMF_적용보고서.md", "DMF_적용보고서.html"]


class ValidationError(ValueError):
    """무결성·입력·경로 검증 실패를 사용자에게 명확히 전달합니다."""


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def checked_path(value, must_exist=True):
    path = Path(value)
    require(path.is_absolute() and ".." not in path.parts, "절대 경로와 상위 이동 없는 경로가 필요합니다")
    # resolve 전에 각 구성 요소를 검사하여 심볼릭 링크와 Windows 정션을 거부합니다.
    for part in reversed((path,) + tuple(path.parents)):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(info.st_mode) and not (getattr(info, "st_file_attributes", 0) & 0x400),
                "심볼릭 링크·정션·reparse point는 허용하지 않습니다")
    if must_exist:
        require(path.exists(), "필수 경로가 없습니다: " + path.name)
    return path.resolve(strict=must_exist)


def safe_child(root, relative, must_exist=True):
    require(isinstance(relative, str) and relative != "", "빈 상대경로는 허용하지 않습니다")
    require(not ntpath.splitdrive(relative)[0] and not relative.startswith(("/", "\\")), "절대 하위경로는 허용하지 않습니다")
    parts = relative.replace("\\", "/").split("/")
    require(all(p not in ("", ".", "..") for p in parts), "하위경로 탈출은 허용하지 않습니다")
    base = checked_path(root)
    result = checked_path(base.joinpath(*parts), must_exist)
    require(result.is_relative_to(base), "루트 밖 경로는 허용하지 않습니다")
    return result


def file_digest(path):
    digest = hashlib.sha256()
    length = 0
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
            length += len(chunk)
    return {"bytes": length, "sha256": digest.hexdigest()}


def git_bytes(root, args, maximum=65536):
    git = shutil.which("git")
    require(git is not None, "Git 실행파일이 필요합니다")
    try:
        run = subprocess.run([git, "-C", str(root)] + args, shell=False, capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValidationError("Git 실행에 실패했습니다: " + type(exc).__name__) from exc
    require(len(run.stdout) <= maximum and len(run.stderr) <= 16384, "Git 응답 크기 상한을 초과했습니다")
    require(run.returncode == 0, "Git 검사 실패: " + run.stderr.decode("utf-8", "replace")[:2000])
    return run.stdout


def load_dmf(root):
    root = checked_path(root)
    require(safe_child(root, ".git").is_dir(), "독립 Git 체크아웃이 필요합니다")
    commit = git_bytes(root, ["rev-parse", "--verify", "HEAD"]).decode("ascii").strip()
    require(commit == DMF_COMMIT, "DMF 커밋이 고정 기준과 다릅니다")
    sources = {}
    dependencies = []
    for name, expected in DMF_BLOBS.items():
        rel = "src/dmf_integrity/" + name
        data = git_bytes(root, ["cat-file", "blob", DMF_COMMIT + ":" + rel])
        require(hashlib.sha256(data).hexdigest() == expected, "DMF 원문 해시 불일치: " + name)
        data.decode("utf-8", errors="strict")
        sources[name] = data
        dependencies.append({"path": rel, "bytes": len(data), "sha256": expected})
    # 작업트리와 __pycache__를 사용하지 않고 검증된 Git blob만 메모리에서 실행합니다.
    package_name = "ict_upstream_dmf_" + DMF_COMMIT[:12]
    package = ModuleType(package_name)
    package.__path__ = []
    sys.modules[package_name] = package
    for name in ("canonical", "merkle", "manifest", "restrict", "merge", "audit_chain"):
        module = ModuleType(package_name + "." + name)
        module.__package__ = package_name
        sys.modules[module.__name__] = module
        exec(compile(sources[name + ".py"], DMF_COMMIT + ":" + name + ".py", "exec"), module.__dict__)
    package.__package__ = package_name
    exec(compile(sources["__init__.py"], DMF_COMMIT + ":__init__.py", "exec"), package.__dict__)
    return SimpleNamespace(**{name: getattr(package, name) for name in package.__all__},
                           AuditEntry=sys.modules[package_name + ".audit_chain"].AuditEntry,
                           ChainBrokenError=sys.modules[package_name + ".audit_chain"].ChainBrokenError,
                           verify_inclusion=sys.modules[package_name + ".merkle"].verify_inclusion,
                           dependency={"url": DMF_URL, "commit": commit, "blobs": dependencies})


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def same_json(actual, expected):
    # Python의 True == 1과 달리 JSON의 불리언·정수 타입을 구분합니다.
    return json_bytes(actual) == json_bytes(expected)


def read_json(root, name):
    path = safe_child(root, name)
    require(path.stat().st_size <= 2 * 1024 * 1024, "JSON 크기 상한을 초과했습니다")

    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "JSON 중복 필드: " + key)
            result[key] = value
        return result

    def forbidden(value):
        raise ValidationError("JSON 실수·비유한 값은 허용하지 않습니다: " + value)

    try:
        return json.loads(path.read_text(encoding="utf-8", errors="strict"), object_pairs_hook=pairs,
                          parse_float=forbidden, parse_constant=forbidden)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError("UTF-8 JSON 해석에 실패했습니다: " + name) from exc


def write_bytes(root, name, data):
    path = safe_child(root, name, False)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as handle:
        handle.write(data)


def grade(index, value):
    if index in (0, 2):
        return 0 if 20 <= value < 26 else 1 if 18 <= value < 28 else 2 if 15 <= value < 30 else 3
    if index in (1, 3):
        return 0 if 40 <= value <= 60 else 1 if 30 <= value <= 70 else 2 if 20 <= value <= 80 else 3
    if index == 4:
        return 0 if value < 800 else 1 if value < 1000 else 2 if value < 1500 else 3
    if index == 5:
        return 0 if value <= 1 else 1 if value == 2 else 2
    return 0 if value <= 15 else 1 if value <= 35 else 2 if value <= 75 else 3


def analyze_csv(path):
    metrics = {key: {"count": 0, "blank": 0, "min": None, "max": None} for key in FIELDS}
    result = {"t": "ict.dmf.analysis/v1", "total_rows": 0, "valid_rows": 0, "invalid_rows": 0,
              "invalid_reasons": {}, "metrics": metrics, "first_timestamp": None, "last_timestamp": None,
              "min_timestamp": None, "max_timestamp": None, "time_zone": "미기록",
              "gaps_over_one_second": 0, "backwards_steps": 0, "adjacent_equal_timestamps": 0,
              "code_level_counts": [0, 0, 0, 0]}
    previous = None
    try:
        with Path(path).open("r", encoding="utf-8", errors="strict", newline="") as handle:
            rows = csv.reader(handle, strict=True)
            require(next(rows, None) == ["timestamp"] + FIELDS, "CSV 열 이름·순서가 원본 계약과 다릅니다")
            for row in rows:
                result["total_rows"] += 1
                reason = None
                values = []
                stamp = None
                if len(row) != 8:
                    reason = "columns"
                else:
                    try:
                        stamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                        require(stamp.strftime("%Y-%m-%d %H:%M:%S") == row[0], "시각 형식 불일치")
                    except (ValueError, ValidationError):
                        reason = "timestamp"
                    if reason is None:
                        try:
                            values = [Decimal(s) if s != "" else None for s in row[1:]]
                            if any(v is not None and not v.is_finite() for v in values):
                                reason = "nonfinite"
                            elif all(v is None for v in values):
                                reason = "all_blank"
                            elif any(values[i] is not None and values[i] != values[i].to_integral_value() for i in (4, 5, 6)):
                                reason = "integer_field"
                        except InvalidOperation:
                            reason = "numeric"
                if reason is not None:
                    result["invalid_rows"] += 1
                    result["invalid_reasons"][reason] = result["invalid_reasons"].get(reason, 0) + 1
                    continue
                result["valid_rows"] += 1
                result["first_timestamp"] = result["first_timestamp"] or row[0]
                result["last_timestamp"] = row[0]
                result["min_timestamp"] = min(result["min_timestamp"] or row[0], row[0])
                result["max_timestamp"] = max(result["max_timestamp"] or row[0], row[0])
                if previous is not None:
                    delta = (stamp - previous).total_seconds()
                    result["gaps_over_one_second"] += int(delta > 1)
                    result["backwards_steps"] += int(delta < 0)
                    result["adjacent_equal_timestamps"] += int(delta == 0)
                previous = stamp
                levels = []
                for index, (key, value) in enumerate(zip(FIELDS, values)):
                    entry = metrics[key]
                    if value is None:
                        entry["blank"] += 1
                        continue
                    entry["count"] += 1
                    entry["min"] = value if entry["min"] is None else min(value, entry["min"])
                    entry["max"] = value if entry["max"] is None else max(value, entry["max"])
                    levels.append(grade(index, value))
                result["code_level_counts"][max(levels)] += 1
    except (UnicodeError, csv.Error) as exc:
        raise ValidationError("CSV UTF-8 또는 인용 형식이 잘못되었습니다") from exc
    for metric in metrics.values():
        for key in ("min", "max"):
            metric[key] = str(metric[key]) if metric[key] is not None else None
    return result


def source_entries(specs):
    return [{**spec, "snapshot_path": "원본보존/" + spec["path"]} for spec in specs]


def expected_modules(api, specs, analysis):
    modules = [api.ModuleRef(s["module_id"], "file", api.Mutability.IMMUTABLE_CORE, i, s["sha256"])
               for i, s in enumerate(specs)]
    modules.append(api.ModuleRef("core.processing", "file", api.Mutability.IMMUTABLE_CORE, 3,
                                 api.content_sha256(json_bytes(POLICY))))
    added = api.ModuleRef("result.analysis", "file", api.Mutability.MUTABLE, 4,
                          api.content_sha256(json_bytes(analysis)), ("source.measurements", "core.processing"))
    return modules, modules + [added]


def expected_versions(api, specs, analysis):
    base, candidate = expected_modules(api, specs, analysis)
    common = {"dc:title": "ICT 안전 수업 실내 공기질 프로젝트", "dmf:dependency_commit": DMF_COMMIT}
    v1 = api.build_version(DOCUMENT_ID, 1, None, base, {**common, "dmf:stage": "원본 최초 봉인"})
    require(api.check_restrictions(base, candidate) == [], "Restrict 변경 제한 위반")
    v2 = api.build_version(DOCUMENT_ID, 2, v1, candidate, {**common, "dmf:stage": "실측 CSV 분석 추가"})
    api.verify_version_chain([v1, v2])
    return [v1, v2]


def versions_json(versions):
    return {"t": "ict.dmf.versions/v1", "versions": [asdict(v) for v in versions]}


def proofs_json(api, version):
    proofs = []
    for module in version.modules:
        index, size, path = api.module_proof(version.modules, module.module_id)
        proofs.append({"module_id": module.module_id, "index": index, "tree_size": size, "path": path})
    return {"t": "ict.dmf.proofs/v1", "manifest_root": version.manifest_root, "proofs": proofs}


def expected_seal(api, specs):
    return {"t": "ict.dmf.sealed/v1", "document_id": DOCUMENT_ID, "dependency": api.dependency,
            "sources": source_entries(specs), "policy_sha256": api.content_sha256(json_bytes(POLICY))}


def validate_locations(source, output, creating=False):
    source = checked_path(source)
    output = checked_path(output, not creating)
    require(source.is_dir(), "원본 루트는 폴더여야 합니다")
    require(not source.is_relative_to(output) and not output.is_relative_to(source), "원본과 출력 경로가 겹칩니다")
    if creating:
        require(not output.exists(), "출력 폴더가 이미 있습니다. 기존 차수를 덮어쓰지 않습니다")
    else:
        require(output.is_dir(), "출력 루트는 폴더여야 합니다")
    return source, output


def verify_data(source, output, api, specs):
    source, output = validate_locations(source, output)
    require(same_json(read_json(output, "봉인_목록.json"), expected_seal(api, specs)), "봉인 목록이 고정 기준과 다릅니다")
    for spec in specs:
        expected = {key: spec[key] for key in ("bytes", "sha256")}
        require(file_digest(safe_child(source, spec["path"])) == expected, "외부 원본 해시·크기가 다릅니다")
        require(file_digest(safe_child(output, "원본보존/" + spec["path"])) == expected, "스냅샷 원문 바이트가 다릅니다")
    require(same_json(read_json(output, "처리_규칙.json"), POLICY), "처리 규칙이 변경됐습니다")
    analysis = analyze_csv(safe_child(output, "원본보존/" + specs[2]["path"]))
    require(analysis["valid_rows"] > 0, "유효 측정 행이 없습니다")
    require(same_json(read_json(output, "분석_결과.json"), analysis), "CSV 재분석 값이 다릅니다")
    versions = expected_versions(api, specs, analysis)
    # 라이브러리가 직접 대조하지 않는 저장 루트·seal·번호·문서 ID까지 전체 필드를 비교합니다.
    require(same_json(read_json(output, "버전_이력.json"), versions_json(versions)), "버전 전체 필드가 재계산 값과 다릅니다")
    proof = read_json(output, "모듈_증명.json")
    require(same_json(proof, proofs_json(api, versions[-1])), "모듈 포함 증명 필드가 다릅니다")
    for module, item in zip(versions[-1].modules, proof["proofs"]):
        require(api.verify_inclusion(module.leaf(), item["index"], item["tree_size"],
                                     [bytes.fromhex(p) for p in item["path"]], bytes.fromhex(versions[-1].manifest_root)),
                "모듈 포함 증명 실패")
    audit = read_json(output, "감사_이력.json")
    require(set(audit) == {"t", "chain_id", "expected_count", "expected_head", "entries"}, "감사 봉투 필드가 다릅니다")
    require(audit["t"] == "ict.dmf.audit/v1" and audit["chain_id"] == DOCUMENT_ID, "감사 체인 ID가 다릅니다")
    require(type(audit["expected_count"]) is int and audit["expected_count"] == len(audit["entries"]) == 2, "감사 이력이 비었거나 삭제됐습니다")
    entries = []
    for i, value in enumerate(audit["entries"]):
        require(value["chain_id"] == DOCUMENT_ID and type(value["seq"]) is int and value["seq"] == i + 1, "감사 순서·문서가 다릅니다")
        require(value["actor"] == "urn:ict:agent:local-adapter" and value["action"] == ("source.snapshot" if i == 0 else "analysis.generated"), "감사 행위가 다릅니다")
        require(value["target"] == "urn:ict:version:" + str(i + 1) and value["ticket_id"] is None, "감사 대상이 다릅니다")
        require(value["detail"] == {"manifest_root": versions[i].manifest_root, "version_hash": versions[i].version_hash}, "감사 대상 해시가 다릅니다")
        require(value["occurred_at"].endswith("Z"), "감사 시각에 UTC 표시가 없습니다")
        datetime.fromisoformat(value["occurred_at"].replace("Z", "+00:00"))
        entries.append(api.AuditEntry(**value))
    require(audit["expected_head"] == [entries[-1].seq, entries[-1].entry_hash], "감사 head가 다릅니다")
    try:
        api.verify_chain(entries, expected_head=tuple(audit["expected_head"]))
    except api.ChainBrokenError as exc:
        raise ValidationError("감사 체인 검사 실패: " + str(exc)) from exc
    result = {"t": "ict.dmf.verification/v1", "verdict": "PASS", "checks": CHECKS,
              "source_file_count": 3, "version_count": 2, "audit_count": 2, "byte_preserved": True,
              "manifest_root": versions[-1].manifest_root, "restrict_seal": versions[-1].restrict_seal,
              "risk_floor": api.risk_floor(versions[0].modules, versions[1].modules), "limitations": LIMITATIONS}
    return result, analysis, versions, audit


def report_sections(analysis, versions, audit, specs):
    metric_rows = [[label, FIELDS[i], unit, str(analysis["metrics"][FIELDS[i]]["count"]),
                    str(analysis["metrics"][FIELDS[i]]["blank"]), str(analysis["metrics"][FIELDS[i]]["min"]),
                    str(analysis["metrics"][FIELDS[i]]["max"])] for i, (label, unit) in enumerate(zip(LABELS, UNITS))]
    return [
        ("적용 대상과 흐름", ["구간", "실제 구성", "DMF 적용"], [
            ["수집", "DHT11·AM1008W-K → Arduino → LCD·RGB LED", "원본 스케치 그대로 봉인"],
            ["기록", "USB 9600 baud → Python → air_log.csv", "수집기와 CSV 원문 바이트 보존"],
            ["검증", "원본 → 스냅샷 → CSV 재분석 → 버전·감사 대조", "로컬 실행형 적용 산출물"]]),
        ("실제 기록 범위", ["항목", "관측값", "해석"], [
            ["전체 데이터 행", str(analysis["total_rows"]), "헤더 제외, 원본 전체 순회"],
            ["유효 / 분석 제외", f"{analysis['valid_rows']} / {analysis['invalid_rows']}", "원본은 제외 행도 그대로 보존"],
            ["첫 기록 / 마지막 기록", f"{analysis['first_timestamp']} / {analysis['last_timestamp']}", "파일 순서 기준, 시간대 미기록"],
            ["1초 초과 인접 간격", str(analysis["gaps_over_one_second"]), "연속 측정 보장을 뜻하지 않음"],
            ["시간 역행 / 인접 같은 시각", f"{analysis['backwards_steps']} / {analysis['adjacent_equal_timestamps']}", "유효 행의 인접 시각 비교"]]),
        ("센서별 관측값", ["항목", "CSV 열", "단위", "숫자 행", "결측 행", "최솟값", "최댓값"], metric_rows),
        ("원본 보존", ["파일", "바이트", "SHA-256"], [[s["path"], str(s["bytes"]), s["sha256"]] for s in specs]),
        ("버전과 제한 검사", ["로컬 버전", "실제 생성 내용", "manifest_root"], [
            ["v1", "원본 세 파일과 처리 규칙의 최초 봉인", versions[0].manifest_root],
            ["v2", "같은 원본에 실측 CSV 분석 추가", versions[1].manifest_root]]),
        ("프로젝트 코드 등급 재현", ["등급", "유효 행 수", "판정 근거"], [
            [label, str(count), "읽힌 센서 항목 중 가장 높은 코드 등급"]
            for label, count in zip(["좋음", "보통", "나쁨", "매우 나쁨"], analysis["code_level_counts"])]),
        ("검증 범위", ["검사", "결과"], [[name, "통과"] for name in CHECKS]),
        ("감사 이력", ["순서", "실제 작업", "UTC 작업시각"], [
            [str(entry["seq"]), entry["action"], entry["occurred_at"]] for entry in audit["entries"]]),
    ]


def render_reports(analysis, versions, audit, specs):
    sections = report_sections(analysis, versions, audit, specs)
    intro = "ICT 안전 수업에서 개발한 실내 공기질 프로젝트의 코드와 측정 원본을 보존하고, DMF의 해시·머클·버전·Restrict·감사 라이브러리를 실제 적용했습니다."
    md = ["# ICT 안전 수업 · 공기질 프로젝트 DMF 적용보고서", "", intro, "",
          "**원본 세 파일의 바이트 보존을 검증했습니다.** v1·v2는 이번 적용 묶음에서 생성한 로컬 버전이며 기존 프로젝트 차수나 과거 편집 기록이 아닙니다.", ""]
    body = ["<header><p class='eyebrow'>ICT 안전 수업 · 수요일 PBL</p><h1>공기질 기록의 출처와 변경을 확인하다</h1><p>" + html.escape(intro) + "</p></header>",
            "<p class='notice'>원본 세 파일의 바이트 보존을 검증했습니다. v1·v2는 이번 적용 묶음의 로컬 버전이며 과거 프로젝트 이력을 만들어 낸 값이 아닙니다.</p>"]
    for title, headers, rows in sections:
        md += ["## " + title, "", "| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for row in rows:
            md.append("| " + " | ".join(str(s).replace("|", "\\|").replace("\n", " ") for s in row) + " |")
        md.append("")
        body.append("<section><h2>" + html.escape(title) + "</h2><div class='table-wrap' tabindex='0'><table><thead><tr>" +
                    "".join("<th scope='col'>" + html.escape(h) + "</th>" for h in headers) + "</tr></thead><tbody>" +
                    "".join("<tr>" + "".join("<td>" + html.escape(str(s)) + "</td>" for s in row) + "</tr>" for row in rows) + "</tbody></table></div></section>")
    explanation = "원본·처리 규칙은 IMMUTABLE_CORE, 추가 분석은 MUTABLE입니다. v1에서 v2로의 Restrict 위반은 없고 위험도 하한은 R1입니다. 이 값은 실제 사람의 승인이나 공식 배포를 뜻하지 않습니다. 숫자 통계는 저장값의 Decimal 문자열을 보존하며 결측 집계의 분모는 유효 행입니다. PDF가 함께 제공되는 경우 HTML의 별도 인쇄 파생본이며 도구 빌드·DMF 체인·파일_무결성.json 범위에서 제외됩니다. PDF 해시는 별도 제출 파일 목록에서 확인합니다."
    source = DMF_URL + "/tree/" + DMF_COMMIT
    md += [explanation, "", "## 적용 범위와 남은 한계", ""] + ["- " + item for item in LIMITATIONS]
    md += ["", "## 재현과 출처", "", "[사용안내](../사용안내.md)에서 build·읽기 전용 verify 명령을 확인할 수 있습니다.", "",
           f"DMF 출처: [{DMF_COMMIT}]({source}). 고정 커밋의 Git blob 7개를 SHA-256으로 검증한 뒤 메모리에서 실행합니다. 작업트리 수정은 실행에 반영되지 않습니다.", "",
           "파일별 원문 바이트 수와 전체 SHA-256은 [파일_무결성.json](파일_무결성.json), 모듈 포함 증명은 [모듈_증명.json](모듈_증명.json)에 있습니다.", ""]
    body += ["<p>" + html.escape(explanation) + "</p><section><h2>적용 범위와 남은 한계</h2><ul>" +
             "".join("<li>" + html.escape(item) + "</li>" for item in LIMITATIONS) + "</ul></section>",
             "<section><h2>재현과 출처</h2><p><a href='../사용안내.md'>실행 안내</a> · <a href='파일_무결성.json'>파일별 SHA-256</a> · <a href='모듈_증명.json'>모듈 포함 증명</a></p><p>고정 Git blob 7개를 SHA-256으로 확인한 뒤 메모리에서 실행합니다. 작업트리 수정은 실행에 반영되지 않습니다.</p><p><a href='" + source + "'>DMF 원문 · " + DMF_COMMIT + "</a></p></section>"]
    css = """@font-face{font-family:NanumGothic;src:url('../assets/NanumGothicBold.ttf') format('truetype');font-weight:700;font-display:swap}*{box-sizing:border-box}html{color-scheme:light dark}body{margin:0;background:#f4f6fa;color:#192536;font-family:NanumGothic,'Nanum Gothic',sans-serif;font-weight:700;line-height:1.8}main{max-width:1180px;margin:0 auto;padding:48px 28px 72px}header{padding:12px 0 26px;border-bottom:3px solid #536f98}h1{font-size:clamp(26px,3.8vw,43px);line-height:1.4;letter-spacing:-.04em;margin:10px 0 20px}h2{font-size:22px;margin:38px 0 12px}p{max-width:1000px}.eyebrow{color:#536f98;font-size:14px}.notice{padding:18px 22px;border-left:4px solid #536f98;background:#e8eef7}.table-wrap{overflow-x:auto;border:1px solid #cbd4df;border-radius:8px;background:white}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:13px 16px;vertical-align:top;border-bottom:1px solid #dfe5ed;min-width:90px;word-break:normal;overflow-wrap:anywhere}th{background:#e9eef5;color:#28415f;white-space:nowrap}tr:last-child td{border-bottom:0}td:first-child{min-width:130px}a{color:#315e9d;text-underline-offset:3px}a:hover{color:#163c70}a:focus-visible,.table-wrap:focus-visible{outline:3px solid #769bd0;outline-offset:3px}li{margin-bottom:12px}@media(max-width:600px){main{padding:26px 16px 48px}h2{font-size:20px}th,td{padding:11px 13px}table{min-width:610px}.notice{padding:14px 16px}}@media(prefers-color-scheme:dark){body{background:#141c27;color:#e0e7f0}.table-wrap{background:#1b2736;border-color:#45566c}th{background:#26374d;color:#dce7f5}td{border-color:#36465b}.notice{background:#223349}a{color:#a8c9f7}a:hover{color:#dceaff}.eyebrow{color:#a8c9f7}}"""
    document = "<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>ICT 안전 수업 공기질 DMF 적용보고서</title><style>" + css + "</style></head><body><main>" + "".join(body) + "</main></body></html>\n"
    return ("\n".join(md)).encode("utf-8"), document.encode("utf-8")


def inventory_names(specs):
    return sorted(JSON_NAMES + REPORT_NAMES + ["원본보존/" + s["path"] for s in specs])


def inventory(root, specs):
    return {"t": "ict.dmf.inventory/v1", "files": [{"path": name, **file_digest(safe_child(root, name))}
                                                  for name in inventory_names(specs)]}


def verify_bundle(source, output, api, specs=SOURCE_SPECS):
    result, analysis, versions, audit = verify_data(source, output, api, specs)
    require(same_json(read_json(output, "검증_결과.json"), result), "검증 결과 JSON이 다릅니다")
    md, page = render_reports(analysis, versions, audit, specs)
    for name, expected in zip(REPORT_NAMES[1:], (md, page)):
        require(safe_child(output, name).read_bytes() == expected, "보고서 원문 바이트가 다릅니다: " + name)
    require(same_json(read_json(output, "파일_무결성.json"), inventory(output, specs)), "산출물 파일별 해시 목록이 다릅니다")
    expected_files = set(inventory_names(specs) + ["파일_무결성.json"])
    actual = set()
    for base, directories, files in os.walk(output, followlinks=False):
        for name in directories + files:
            checked_path(Path(base) / name)
        for name in files:
            actual.add((Path(base) / name).relative_to(output).as_posix())
    # PDF는 부모의 별도 렌더링·해시 검증 대상으로, 로컬 도구의 필수 산출물로 만들지 않습니다.
    actual.discard("DMF_적용보고서.pdf")
    require(actual == expected_files, "산출물 파일 목록이 고정 목록과 다릅니다")
    return result


def build_bundle(source, output, api, specs=SOURCE_SPECS):
    source, output = validate_locations(source, output, creating=True)
    for spec in specs:
        require(file_digest(safe_child(source, spec["path"])) == {key: spec[key] for key in ("bytes", "sha256")}, "원본이 고정 기준과 다릅니다")
    analysis = analyze_csv(safe_child(source, specs[2]["path"]))
    require(analysis["valid_rows"] > 0, "유효 측정 행이 없습니다")
    versions = expected_versions(api, specs, analysis)
    output.mkdir(parents=True, exist_ok=False)
    for spec in specs:
        original = safe_child(source, spec["path"])
        destination = safe_child(output, "원본보존/" + spec["path"], False)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with original.open("rb") as src, destination.open("xb") as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
    audit = api.AuditChain(DOCUMENT_ID)
    for i, version in enumerate(versions):
        audit.append(occurred_at=datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z"),
                     actor="urn:ict:agent:local-adapter", action="source.snapshot" if i == 0 else "analysis.generated",
                     target="urn:ict:version:" + str(i + 1),
                     detail={"manifest_root": version.manifest_root, "version_hash": version.version_hash})
    audit_json = {"t": "ict.dmf.audit/v1", "chain_id": DOCUMENT_ID, "expected_count": 2,
                  "expected_head": list(audit.head), "entries": [asdict(entry) for entry in audit.entries]}
    values = [expected_seal(api, specs), POLICY, analysis, versions_json(versions), audit_json, proofs_json(api, versions[-1])]
    for name, value in zip(JSON_NAMES, values):
        write_bytes(output, name, json_bytes(value))
    result, checked_analysis, checked_versions, checked_audit = verify_data(source, output, api, specs)
    write_bytes(output, "검증_결과.json", json_bytes(result))
    md, page = render_reports(checked_analysis, checked_versions, checked_audit, specs)
    write_bytes(output, "DMF_적용보고서.md", md)
    write_bytes(output, "DMF_적용보고서.html", page)
    write_bytes(output, "파일_무결성.json", json_bytes(inventory(output, specs)))
    return verify_bundle(source, output, api, specs)


def main(argv=None):
    parser = argparse.ArgumentParser(description="원본 공기질 코드·CSV를 보존하고 DMF 무결성 증거를 생성·검증합니다")
    parser.add_argument("command", choices=("build", "verify"), help="build: 새 산출물 생성 / verify: 파일 변경 없는 재검증")
    parser.add_argument("--source-root", required=True, type=Path, help="기존 코드/최종 원본 폴더")
    parser.add_argument("--output", required=True, type=Path, help="새 차수의 실행결과 폴더")
    parser.add_argument("--dmf-root", required=True, type=Path, help="고정 커밋의 외부 DMF 체크아웃")
    args = parser.parse_args(argv)
    try:
        api = load_dmf(args.dmf_root)
        result = (build_bundle if args.command == "build" else verify_bundle)(args.source_root, args.output, api)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValidationError, OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        print("검증 실패: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
