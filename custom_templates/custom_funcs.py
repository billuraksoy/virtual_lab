from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
def TreatmentVars(self):
    if hasattr(self,'session'):#make sure this is only called on things it would work for
        return dict(
            threshold_high = self.session.config['threshold_high'],
            threshold_low = self.session.config['threshold_low'],
            value_high = self.session.config['value_high'],
            value_low = self.session.config['value_low'],
            total_rounds = self.session.config['total_rounds'],
            group_size = self.session.config['group_size'],
            waiting_room_lowerlimit=self.session.config['waiting_room_lowerlimit'],
            simultaneous = self.session.config['simultaneous'],
            base_tokens = self.session.config['base_tokens'],
            increment = self.session.config['increment'],
            decision_timer = self.session.config['decision_timer'],
            participation_payment = self.session.config['participation_payment']
            );
def participant_vars_dump(self,page):
    if self.participant.vars.get('vars_json_dump',None)==None:#if this doesn't exist
        self.participant.vars['vars_json_dump']=dict()
    for field in page.form_fields:
        page_name = page.get_template_names()[-1].split("/")[-1].split(".")[0]#in the format "app/page.html" extracts just "page"
        self.participant.vars['vars_json_dump'][page_name+'-'+field+('-'+str(self.round_number)) if (not self.round_number==-1) else ""]=str(getattr(self, field))

BasePlayer.TreatmentVars=TreatmentVars
BasePlayer.participant_vars_dump = participant_vars_dump