from security_analyzer.services.classifier import classify_log


def test_critical_rule_matches_case_insensitively():
    assert classify_log("MALWARE CONFIRMED")[0] == "critical"


def test_high_rule_matches_brute_force():
    assert classify_log("Possible brute force attack")[0] == "high"


def test_more_severe_rule_wins():
    assert classify_log("ransomware after failed login")[0] == "critical"


def test_unknown_log_is_info():
    assert classify_log("Routine backup completed")[0] == "info"
