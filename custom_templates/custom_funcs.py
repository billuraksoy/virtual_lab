def TreatmentVars(self):
    # if(self.session.config['synchronous_game']):
    #     N=0
    #     for a in self.session.get_participants():
    #         if a.vars.get('timed_out', None) == False:
    #             if a.vars.get('groupmate_timed_out', False)==False:
    #                 N+=1
    #     wrll=N#in this case the min in waiting room is the number in session
    # else:
    wrll=self.session.config['waiting_room_lowerlimit']
    return dict(
        threshold_high = self.session.config['threshold_high'],
        threshold_low = self.session.config['threshold_low'],
        value_high = self.session.config['value_high'],
        value_low = self.session.config['value_low'],
        total_rounds = self.session.config['total_rounds'],
        group_size = self.session.config['group_size'],
        waiting_room_lowerlimit=wrll,
        simultaneous = self.session.config['simultaneous'],
        base_tokens = self.session.config['base_tokens'],
        increment = self.session.config['increment'],
        decision_timer = self.session.config['decision_timer'],
        participation_payment = self.session.config['participation_payment']
        );