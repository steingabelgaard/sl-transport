CREATE OR REPLACE VIEW transport_registration_view AS (
    SELECT eqr.id as id,
           eqr.event_registration_id as participant_id,
           eqr.event_question_option_id as camp_day_id,
           CONCAT(er.name, ' - ', eqo.name) as name,
           er.registration_master_id as registration_master_id,
           esca.subcamp_id as subcamp_id,
           mr.subcamp_area_id as subcamp_area_id,
           mr.scout_organization as scout_organization,
           mr.state as master_state,
           er.state as participant_state
    FROM event_question_response eqr
    JOIN event_question eq ON eq.id = eqr.event_question_id AND eq.name = 'Lejrdøgn'
    JOIN event_question_option eqo ON eqo.id = eqr.event_question_option_id
    JOIN event_registration er on er.id = eqr.event_registration_id AND er.master = 'f'
    JOIN event_registration mr on mr.id = er.registration_master_id AND mr.master = 't'
    LEFT JOIN event_subcamp_area esca on esca.id = mr.subcamp_area_id
)
