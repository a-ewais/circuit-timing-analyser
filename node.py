from pin import Pin


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
        if type == 'input':
            self.delay = 0.0001
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

    def get_out_transition(self):
        if self.output_transition is not None:
            return self.output_transition
        self.output_transition = -9999999999
        for name, pin in self.input_pins.items():
            # print('transition', self.index,name,pin.get_output_transition(
            #     self.output_net_capacitance + pin.pin_capacitance, self.graph.get_node(pin.connected_to).get_out_transition()) )
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

            self.delay = max(self.delay, pin.get_delay(self.output_net_capacitance + pin.pin_capacitance,
                                                       self.graph.get_node(pin.connected_to).get_out_transition()))
        return self.delay

