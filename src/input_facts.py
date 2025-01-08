facts = """
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% GENERAL FACTS

%% proceeding_type(PersonId, _criminal)
%
% The proceedings are of criminal nature
%

proceeding_type(PersonId, criminal).


%% proceeding_type(PersonId, _europeanArrestWarrant)
%
% The proceedings concern the execution of a european arrest warrant
%

proceeding_type(PersonId, europeanArrestWarrant).


%% person_status(PersonId, _suspect)
%
% The person is a suspect
%

person_status(PersonId, suspect).


%% person_status(PersonId, _accused)
%
% The person is an accused
%

person_status(PersonId, accused).


%% person_made_aware(PersonId, _personStatus)
%
% The person has been made aware of his status
%

person_made_aware(PersonId, personStatus).


%% proceeding_status(PersonId, _started)
%
% The proceedings have started
%

proceeding_status(PersonId, started).

"""

facts_dir_2010_64 = """
Directive 2010_64
%% person_document(PersonId, _europeanArrestWarrant)
%
% The document issued is the european arrest warrant
%

person_document(PersonId, europeanArrestWarrant).


%% authority_decision(PersonId, _essential_document)
%
% The authority has decreed any document to be essential
%

authority_decision(PersonId, essential_document).


%% person_request_submitted(PersonId, _essential_document)
%
% The person has submitted a request to consider a document to be essential
%

person_request_submitted(PersonId, essential_document).


%% person_document(PersonId, _document_deprives_liberty)
%
% The document issued is any document that deprives liberty
%

person_document(PersonId, document_deprives_liberty).


%% person_document(PersonId, _charge)
%
% The document issued is the charge
%

person_document(PersonId, charge).


%% person_document(PersonId, _indictment)
%
% The document issued is an indictment
%

person_document(PersonId, indictment).


%% person_document(PersonId, _judgement)
%
% The document issued is a judgement
%

person_document(PersonId, judgement).

%% person_speaks(PersonId, Language).
%
% The person speaks language X
%

person_speaks(PersonId, Language)

%% person_understands(PersonId, Language)
%
% The person reads and understands language X
%

person_understands(PersonId, Language).

%% lawyer_language(PersonId, Language)
%
% The lawyer can speak, read and understand this language
%

lawyer_language(PersonId, Language).


%% proceeding_language(PersonId, Language)
%
% The language of the proceedings is X
%

proceeding_language(PersonId, Language).
"""

facts_dir_2013_48 = """

%% person_status(PersonId, _requested)
%
% The person is requested under an european arrest warrant
%

person_status(PersonId, requested).


%% person_status(PersonId, _deprived_of_liberty)
%
% The person has been deprived of liberty
%

person_status(PersonId, deprived_of_liberty).


%% proceeding_matter(PersonId, _questioning)
%
% The defendant has been subject to questioning
%

proceeding_matter(PersonId, questioning).


%% proceeding_matter(PersonId, _evidence_gathering_act)
%
% The proceedings concern any evidence gathering act
%

proceeding_matter(PersonId, evidence_gathering_act).


%% proceeding_matter(PersonId, _summoned_court)
%
% The proceedings concern the summon to court of the person
%

proceeding_matter(PersonId, summoned_court).


%% proceeding_matter(PersonId, _pre_trial)
%
% The proceedings are happening before the trial has started
%

proceeding_matter(PersonId, pre_trial).


%% person_event(PersonId, _geographical_remoteness)
%
% The person's geographical remoteness makes it impossible to ensure no delay to the presence of the lawyer
%

person_event(PersonId, geographical_remoteness).


%% person_nominate(PersonId, PersonId2)
%
% The person would like to nominate X as a third person to communicate with
%

person_nominate(PersonId, PersonId2).


%% person_danger(PersonId, _life)
%
% There is need to avoid damage to a person's life
%

person_danger(PersonId, life).


%% person_danger(PersonId, _liberty)
%
% There is need to avoid damage to a person's liberty
%

person_danger(PersonId, liberty).


%% person_danger(PersonId, _physical_integrity)
%
% There is need to avoid damage to a person's physical integrity
%

person_danger(PersonId, physical_integrity).


%% proceeding_danger(PersonId, _substantially_jeopardised)
%
% There is danger of the proceedings being substantially jeopardised
%

proceeding_danger(PersonId, substantially_jeopardised).


%% proceeding_country(PersonId, Country)
%
% The proceedings are located in country X
%

proceeding_country(PersonId, Country).


%% person_nationality(PersonId, Country)
%
% The person is of nationality X
%

person_nationality(PersonId, Country).


%% proceeding_matter(PersonId, _hearing)
%
% The proceedings concern an hearing
%

proceeding_matter(PersonId, hearing).

"""



facts_dir_2016_800 = """
% Directive 2016/800

%% person_status(PersonId, _child)
%
% The person is a child
%

person_status(PersonId, child).


%% person_status(PersonId, _subject_to_proceedings)
%
% The person is the subject of the proceedings
%

person_status(PersonId, subject_to_proceedings).


%% person_age(PersonId, Age, _start_proceeding)
%
% The person was X years of age at the start of the proceedings
%

person_age(PersonId, Age, start_proceeding).


%% person_age(PersonId, Age)
%
% The person is currently X years of age
%

person_age(PersonId, Age).


%% person_status(PersonId, _deprived_of_liberty)
%
% The person has been deprived of liberty
%

person_status(PersonId, deprived_of_liberty).


%% person_nature(PersonId, _natural)
%
% The person is a natural person
%

person_nature(PersonId, natural).


%% person_nature(PersonId, _legal)
%
% The person is a legal person
%

person_nature(PersonId, legal).


%% holds_parental_responsibility(PersonId, ChildId)
%
% This person holds parental responsibility over the child
%

holds_parental_responsibility(HolderId, PersonId).



%% responsibility_assigned(PersonId, ChildId, _judgement)
%
% The responsiblity over the child has been assigned through a judgement
%

responsibility_assigned(PersonId, ChildId, judgement).


%% responsibility_assigned(PersonId, ChildId, _operation_of_law)
%
% The responsiblity over the child has been assigned through an operation of law
%

responsibility_assigned(PersonId, ChildId, operation_of_law).


%% responsibility_assigned(PersonId, ChildId, _agreement_having_legal_effects)
%
% The responsiblity over the child has been assigned through an agreement having legal effect
%

responsibility_assigned(PersonId, ChildId, agreement_having_legal_effects).


%% person_status(PersonId, _age_unknown)
%
% The person's age is unknown
%

person_status(PersonId, age_unknown).


%% proceeding_matter(PersonId, _court_hearing)
%
% The proceedings concern the court hearing
%

proceeding_matter(PersonId, court_hearing).


%% proceeding_matter(PersonId, _questioning)
%
% The defendant has been subject to questioning
%

proceeding_matter(PersonId, questioning).


%% proceeding_matter(PersonId, _evidence_gathering_act)
%
% The proceedings concern any evidence gathering act
%

proceeding_matter(PersonId, evidence_gathering_act).


%% proceeding_matter(PersonId, _summoned_court)
%
% The proceedings concern the summon to court of the person
%

proceeding_matter(PersonId, summoned_court).


%% proceeding_matter(PersonId, _identity_parade)
%
% The proceedings concern an identity parade
%

proceeding_matter(PersonId, identity_parade).


%% proceeding_matter(PersonId, _confrontations)
%
% The proceedings concern confrontation
%

proceeding_matter(PersonId, confrontations).


%% proceeding_matter(PersonId, _reconstructions_crime_scene)
%
% The proceedings concern the reconstructions of a crime scene
%

proceeding_matter(PersonId, reconstructions_crime_scene).

%% holder_nomination(ChildId, HolderId)
%
% The child has nominated someone as holder of parental responsibility
%

holder_nomination(ChildId, HolderId).


%% authority_decision(PersonId, _accepted)
%
% The authority has accepted the nomination of the child concerning the holder of parental responsibility
%

authority_decision(PersonId, accepted).


%% authority_nominates(PersonId, HolderId)
%
% The authority has nominated someone to accompany the child as responsibility holder
%

authority_nominates(PersonId, HolderId).


%% person_status(HolderId, _holder_of_parental_responsibility)
%
% The person is an holder of parental responsibility
%

person_status(HolderId, holder_of_parental_responsibility).


%% contrary_to_child_interest(PersonId)
%
% The person is acting contrary to the interests of the child
%

contrary_to_child_interest(PersonId).


%% jeopardises_proceedings(HolderId)
%
% This person's acting jeopardises the proceedings
%

jeopardises_proceedings(HolderId).

%% authority_decision(HolderId, _nomination)
%
% The authority has nominated a new holder of parental responsibility
%

authority_decision(HolderId, nomination).


%% proceeding_matter(PersonId, _detention)
%
% The proceedings concern detention
%

proceeding_matter(PersonId, detention).


%% person_status(PersonId, _detained)
%
% The person has been detained
%

person_status(PersonId, detained).


%% person_status(PersonId, _specific_health_indications)
%
% The person is in need of specific health indications
%

person_status(PersonId, specific_health_indications).


%% person_request_submitted(PersonId, _medical_exam)
%
% The person has submitted a request to perform a medical exam
%

person_request_submitted(PersonId, medical_exam).


%% person_request_submitted(HolderId, _medical_exam)
%
% The holder of parental responsibility has submitted a request to perform a medical exam
%

person_request_submitted(HolderId, medical_exam).


%% person_request_submitted(PersonId, _lawyer_medical_exam)
%
% The person's lawyer has submitted a request to perform a medical exam
%

person_request_submitted(PersonId, lawyer_medical_exam).


%% person_danger(PersonId, _life)
%
% There is need to avoid damage to someone's life
%

person_danger(PersonId, life).


%% person_danger(PersonId, _liberty)
%
% There is need to avoid damage to someone's liberty
%

person_danger(PersonId, liberty).


%% person_danger(PersonId, _physical_integrity)
%
% There is need to avoid damage to someone's physical integrity
%

person_danger(PersonId, physical_integrity).


%% proceeding_matter(PersonId, _pre_trial)
%
% The proceedings are happening before the trial has started
%

proceeding_matter(PersonId, pre_trial).


%% imperative_immediate_action(PersonId, _investigating_authority)
%
% Investigating authority must intervene to avoid jeopardising the proceedings
%

imperative_immediate_action(PersonId, investigating_authority).


%% proceeding_matter(PersonId, _trial_in_absentia)
%
% The proceedings have been conducted in absentia
%

proceeding_matter(PersonId, trial_in_absentia).
"""

dir_facts = {
    "directive_2010_64" : facts_dir_2010_64,
    "directive_2013_48" : facts_dir_2013_48
}