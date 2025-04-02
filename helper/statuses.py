import enum


class Status(enum.Enum):
    placement_new = {
        'num': 7,
        'transitions': [
            'in_work',
            'completed',
        ],
    }

    def __init__(self, vals):
        self.num = vals['num']
        self.transitions = vals['transitions']

    def can_transition(self, new_state):
        return new_state.name in self.transitions


class CampaignStatus(enum.Enum):
    new = {
        'num': 7,
        'transitions': {
            'draft': 'Черновик',
            'planning': 'Планирование',
            'approved': 'Утверждено',
            'filled_in': 'Заполнено',
            'published': 'Опубликована',
        },
    }
    in_progress = {
        'num': 6,
        'transitions': [
            'started',
            'completed',
            'deleted',
            'canceled',
        ],
    }

    def __init__(self, vals):
        self.num = vals['num']
        self.transitions = vals['transitions']

    def can_transition(self, new_state):
        return new_state.name in self.transitions


print('------------------------------------------------')
print('Name CampaignStatus:', CampaignStatus.in_progress)
print('Value CampaignStatus:', CampaignStatus.in_progress.value)
print(
    'Custom attribute CampaignStatus:', CampaignStatus.in_progress.transitions
)
print(
    'Custom attribute New Transitions CampaignStatus:',
    CampaignStatus.new.transitions,
)
print(
    'Using attribute CampaignStatus:',
    CampaignStatus.in_progress.can_transition(CampaignStatus.new),
)
