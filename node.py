from pin import Pin
from scipy import interpolate

class Node:
    # delay the delay for this node
    # type the type of the gate
    # graph pointer to the parent graph
    # input_pins dictionary of the pins connected to the gate
    '''you can use pin.connected_to to get the gate connected to this pin'''

    def __init__(self, index, type, pins, Graph):
        self.graph = Graph
        self.index = index
        self.type = type
        self.name = type + "_" + index
        self.input_pins = {}
        self.skew = 0
        self.clock = 0
        self.setup = 0
        self.hold = 0
        if type == 'input':
            self.delay = Graph.timing_constraints['input_delay']
            self.output_transition = 0.5
            self.output_net_capacitance = 0
            return

        for name, input_pin in pins.items():
            if name != 'Y' and name != 'Q':
                self.input_pins[name] = Pin(input_pin, name)

        self.output_net_capacitance = 0.04  # assumption
        if 'Y' in pins.keys():
            self.output_pins = Pin(pins['Y'], 'Y', type='output')
        elif 'Q' in pins.keys():
            self.output_pins = Pin(pins['Q'], 'Q', type='output')
        self.delay = None
        self.output_transition = None

    def handle_ff(self,ff_info):
        if type == 'DFFPOSX1':
            self.get_setup(ff_info)
            self.get_hold(ff_info)
            self.skew = self.graph.skews[self.name]
            self.clock = self.graph.timing_constraints['clock_period']



    def get_setup(self, ff_info):
        setup = [[max(ff_info['setup_rise']['table'][str(x)][str(y)], ff_info['setup_fall']['table'][str(x)][str(y)])
                  for y in ff_info['setup_rise']['x_values']] for x in ff_info['setup_rise']['y_values']]
        setup = interpolate.interp2d(ff_info['setup_rise']['x_values'], ff_info['setup_rise']['y_values'],
                                    setup, bounds_error=False, copy=False)
        self.setup = setup(self.skew, self.graph.get_node(self.input_pins['D'].connected_to).get_out_transition())[0]


    def get_hold(self,ff_info):
        hold = [[min(ff_info['hold_rise']['table'][str(x)][str(y)],ff_info['hold_fall']['table'][str(x)][str(y)])
                  for y in ff_info['hold_rise']['x_values']]for x in ff_info['hold_rise']['y_values']]
        hold = interpolate.interp2d(ff_info['hold_rise']['x_values'], ff_info['hold_rise']['y_values'],
                                 hold, bounds_error=False, copy=False)
        self.hold = hold(self.skew, self.graph.get_node(self.input_pins['D'].connected_to).get_out_transition())[0]

    def get_out_transition(self):
        if self.output_transition is not None:
            return self.output_transition
        self.output_transition = -9999999999
        for name, pin in self.input_pins.items():
            # print('transition', self.index,name,pin.get_output_transition(
            #     self.output_net_capacitance + pin.pin_capacitance, self.graph.get_node(pin.connected_to).get_out_transition()) )
            if name != 'D':
                self.output_transition = max(self.output_transition, pin.get_output_transition(
                    self.output_net_capacitance + pin.pin_capacitance,
                    self.graph.get_node(pin.connected_to).get_out_transition()))
        return self.output_transition


    def get_delay(self):
        if self.delay is not None:
            return self.delay
        self.delay = -99999999999
        for name, pin in self.input_pins.items():
            # print('delay' ,self.index, name,pin.get_delay(self.output_net_capacitance+ pin.pin_capacitance,
            #                                        self.graph.get_node(pin.connected_to).get_out_transition()))
            if name != 'D':
                self.delay = max(self.delay, pin.get_delay(self.output_net_capacitance + pin.pin_capacitance,
                                                       self.graph.get_node(pin.connected_to).get_out_transition()))
        return self.delay

    def check_constraints(self,t_cont,t_prob,tcq,s_skew):
        '''true if we have a violation, this function is always called at the receiver flipflop
        not the sender.......slacks are positive if '''
        slack = self.setup + s_skew + tcq + t_prob - (self.clock + self.skew)
        if (self.setup + s_skew + tcq + t_prob <= self.clock + self.skew):
            setup = False
        else:
            setup = True

        if (self.hold + self.skew <= tcq + t_cont + s_skew):
            hold = False
        else:
            hold = True

        return hold, setup, slack