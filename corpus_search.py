SEARCH_DICTIONARY = {
    'search_attorney': r'(\. .{3,100}? for defendants?)',
    'search_appointed': r'under appointment',
    'search_outcome':r'(judgm?en?t?\. .{3,100}?\.)',
    'pitchess_motion': r'pitchess .{0,5}?motion',
    'prejudice':'unduly prejudicial',
    'no_error':'no error',
    'mid_term': r'mid(dle)?[ -]?term',
    'disposition': r'disposition .{0:100}?\.',
    'full_disposition':r'disposition.{0:100}?not to be published',
    'prior_conviction': r'prior .{3,20}conviction',
    'prior_felony_conviction': r'prior felony convictions?',
    'ineffective_assistance': r'ineffective assistance',
    'habeas_corpus': r'habeas corpus',
    'prosecutorial_misconduct': r'(prosecutor|prosecutorial) misconduct',
    'polygraph': 'polygraph',
    'kamala_harris': r'kamala .{0,10}?harris',
    'constitutional_violation': r'constitutional violation',
    'three_strikes':r'(?:three|3)(?:\s|-)strikes?'
    'enhancement':r'(?:firearm|strikes|felony) enhancements?',    'any_enhancement':r'[\w+]{3,20}\senhancement\b\s?[\w+]{3,20}',    'term':r'\b[\w+]*\b(?:\s|-)?term'
    'resentencing':r're-?sentenc'
    }

MORE_TERMS = {
    'felony':r'felon(y|ies)',
    'three_strikes':r'(three|3) ?-?strikes'
    }

SEARCH_TERMS = [
    'felony',
    'three strikes',
    'prior conviction',
    '3 strikes',
    'strikes enhancement',
    'kamala harris',
    'firearm',
    'firearm enhancement',
    'sentencing',
    'high term',
    'low term',
    'mid term',
    'habeas corpus',
    'prior convictions',
    'reversed',
    'remanded',
    'affirmed',
    'serious felony',
    'strike',
    'to life',
    'years life',
    'assault',
    'deadly weapon',
    'murder',
    'felony enhancements',
    'felony enhancement',
    'guilty plea',
    'resentencing',
    'under appointment',
    'no appearance',
    'affirm',
    'determinate term',
    'indeterminate term',
    'raised no',
    'no issues',
    'felony priors',
    'strikes law',
    'second strike',
    'third strike',
    'enhancement',
    'ineffective assistance'
]


# Info we want about a case
# Outcome, defendant, LA cty casenum, trial court lawyer, appeals court lawyer
# Presiding judge, type of crime, past history, date

# Want to be able to maintain set of cases with...
#    0/1 dataframe of whether thing occurs or not
#    Want to be able to add things on to that df
#    Preserved list of content

# maybe case object has properties
#    appeals_case_number
#    superior_case_number
#    pdf_path
#    scanned_text_path
#    clean_text_path
#    scanned_text
#    clean_text
#    occurrence_dict
#    occurrence_df
# want to separate things into "stuff we want to access the case by" and
# stuff we want to be able to put in a dataframe to compare all cases by
# so we actually also want the occurrence_dict to have the case numbers etc. as
# well

# we also want to be able to save an object or a list of objects easily


class Case:
    occurrence_dict = {}
    # Note to self: These are class elements, so if you want to change them,
    # you can change the whole class by setting Case.<element> = <value>
    # and change individual cases with case.<element> = value
    def __init__(self):
        pass
    def set_scanned_text_path(self, scanned_text_path):
        self.scanned_text_path = scanned_text_path
    def read_scanned_text(self):
        assert os.path.isfile(self.scanned_text_path) == True
        with open(self.scanned_text_path, "r") as file:
            self.scanned_text = file.read()
            self.appeals_case_number = os.path.splitext(os.path.split(self.scanned_text_path)[1])[0]
            self.occurrence_df = pd.DataFrame(index=[self.appeals_case_number])
    def set_clean_text_path(self, clean_text_path):
        self.clean_text_path = clean_text_path
    def read_clean_text(self):
        assert os.path.isfile(self.clean_text_path) == True
        with open(self.clean_text_path, "r") as file:
            self.clean_text = file.read()
            self.appeals_case_number = os.path.splitext(os.path.split(self.clean_text_path)[1])[0]
            self.occurrence_df = pd.DataFrame(index=[self.appeals_case_number])
    def make_clean_text(self):
        text = self.scanned_text
        text = text.lower()
        # Strip all newlines:
        text = re.sub('\n', '', text)
        # turn all whitespace into single spaces:
        self.clean_text = re.sub(r'(\s+)', ' ', text)
    # TODO: either merge the text functions or have them check if casenum
    # already exists?
    def set_pdf_path(self, pdf_path):
        assert os.path.isfile(pdf_path) == True, \
            "pdf_path must lead to a file."
        self.pdf_path = pdf_path
    def set_save_path(self):
        assert (self.appeals_case_number is not None), \
            "Appeals case number must be set before object can be saved."
        current_path = os.path.abspath('')
        folder = os.path.join(current_path, 'case_objects')
        save_path = os.path.join(folder,'%s.bin' % self.appeals_case_number)
        self.save_path = save_path
    def save(self):
        with open(self.save_path, 'wb') as f:
            pickle.dump(self, f)
        # TODO: test read/write from binary

# want a function that takes a dict {key:value}, searches for value,
# if found: puts the result in column "key" in DataFrame
# if not: puts ... None? False? 'Not found?'

    def find(self, search_dictionary):
    # search_dictionary should be of form {'category':'regex'}
        assert (self.clean_text is not None), \
            'Cleaned text must be available to search.'
        assert (len(search_dictionary) != 0), \
            'Size of dictionary is zero. Dictionary must have contents.'
        text = self.clean_text
        for key in search_dictionary:
            found = re.findall(search_dictionary[key], text)
            if len(found) != 0:
                self.occurrence_df[key] = 1
                self.occurrence_dict[key] = found
            else:
                self.occurrence_df[key] = 0
                self.occurrence_dict[key] = 'Not found'



# to initialize a case:
