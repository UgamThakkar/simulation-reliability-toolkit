from sim import run_simulation, SUCCESS, BAD_INPUT

def test_bad_input_returns_error_code():
    assert run_simulation(steps=0) == BAD_INPUT

def test_small_run_succeeds():
    assert run_simulation(steps=5) == SUCCESS