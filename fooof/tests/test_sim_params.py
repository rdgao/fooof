"""Test functions for fooof.sim.params."""

from py.test import raises

from fooof.sim.params import *

###################################################################################################
###################################################################################################

def test_update_sim_ap_params():

    sim_params = SimParams([1, 1], [10, 1, 1], 0.05)

    # Check updating of a single specified parameter
    new_sim_params = update_sim_ap_params(sim_params, 1, 'exponent')
    assert new_sim_params.aperiodic_params == [1, 2]

    # Check updating of multiple specified parameters
    new_sim_params = update_sim_ap_params(sim_params, [1, 1], ['offset', 'exponent'])
    assert new_sim_params.aperiodic_params == [2, 2]

    # Check updating of all parameters
    new_sim_params = update_sim_ap_params(sim_params, [1, 1])
    assert new_sim_params.aperiodic_params == [2, 2]

    # Check error with invalid overwrite
    with raises(ValueError):
        new_sim_params = update_sim_ap_params(sim_params, [1, 1, 1])

def test_stepper():

    stepper = Stepper(8, 12, 1)
    assert stepper
    assert len(stepper) == 4
    for val in stepper:
        assert True

def test_stepper_errors():
    """Test the checks in Stepper._check_values()"""

    with raises(ValueError):
        Stepper(-1, 0, 0)

    with raises(ValueError):
        Stepper(10, 8, 1)

    with raises(ValueError):
        Stepper(8, 12, 5)

def test_param_iter():

    # Test oscillations
    step = Stepper(8, 12, .1)
    osc = [step, .5, .5]
    iter_1 = param_iter(osc)

    for ind, val in enumerate(iter_1):
        assert val == [8 + (.1*ind), .5, .5]

    # Test aperiodic
    step = Stepper(.25, 3, .25)
    ap_params = [0, step]
    iter_1 = param_iter(ap_params)

    for ind, val in enumerate(iter_1):
        assert val == [0, .25 + (.25*ind)]

    # Test n oscillations
    step = Stepper(8, 12, .1)
    oscs = [step, .5, .5, 10, .25, 1]
    iter_1 = param_iter(oscs)

    for ind, val in enumerate(iter_1):
        assert val == [8 + (.1*ind), .5, .5, 10, .25, 1]

    # Test list of lists
    step = Stepper(8, 12, .1)
    osc_1 = [1, 2, 3]
    osc_2 = [4, 5, 6]
    osc_3 = [7, 8, step]
    oscs = [osc_1, osc_2, osc_3]
    iter_2 = param_iter(oscs)

    for ind, val in enumerate(iter_2):
        assert val == [1, 2, 3, 4, 5, 6, 7, 8, 8 + (.1*ind)]

    # Test multiple stepper error
    step = Stepper(8, 12, .1)
    with raises(ValueError):
        for params in param_iter([[step, step, step]]): pass

def test_param_sampler():

    pos = [1, 2, 3, 4]
    gen = param_sampler(pos)

    for ind, el in zip(range(3), gen):
        assert el in pos
