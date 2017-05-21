from scipy import interpolate


class Pin:
    def __init__(self, pin, name, type='input'):
        self.name = name
        self.connected_to = str(pin['connected_to'][0])
        if type == 'output':
            return
        self.pin_capacitance = pin['capacitance']
        if 'cell_rise' in pin.keys():
            self.x_values = pin['cell_rise']['x_values']
            self.y_values = pin['cell_rise']['y_values']
            # print(self.x_values)
            # print(self.y_values)
            # print(pin['cell_rise']['table'])
            # print(pin['cell_fall']['table'])
            # [[print(x,y)for y in self.x_values ]for x in self.y_values]
            self.delay = [[max(pin['cell_rise']['table'][str(x)][str(y)], pin['cell_fall']['table'][str(x)][str(y)])
                           for y in self.x_values] for x in self.y_values]
            self.transition = [
                [max(pin['rise_transition']['table'][str(x)][str(y)], pin['fall_transition']['table'][str(x)][str(y)])
                 for y in self.x_values] for x in self.y_values]

    def get_output_transition(self, total_output_net_capacitance, input_transision):
        f = interpolate.interp2d(self.x_values, self.y_values, self.transition, bounds_error=False, copy=False)
        # print(f(input_transision,total_output_net_capacitance)[0])
        return f(input_transision, total_output_net_capacitance)[0]

    def get_delay(self, total_output_net_capacitance, input_transision):
        print(self.name,self.connected_to)
        f = interpolate.interp2d(self.x_values, self.y_values, self.delay, bounds_error=False, copy=False)
        # print(f(input_transision,total_output_net_capacitance)[0])
        return f(input_transision, total_output_net_capacitance)[0]

