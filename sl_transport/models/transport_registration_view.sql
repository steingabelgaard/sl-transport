CREATE OR REPLACE VIEW transport_registration_view AS (
select er.id ,er.name, COALESCE(er.registration_master_id,er.id) as master_id,COALESCE(er.partner_id,erm.partner_id) as partner_id, er.associated_group_id,
COALESCE(erm.country_id,er.country_id) as country_id,er.event_id,  
sca.subcamp_id, 
case when sca.subcamp_id = 1 then 'Brandhøjgårdsvej'  when sca.subcamp_id = 2 then 'Brandhøjgårdsvej' when  sca.subcamp_id = 3 then 'P-plads Vindingevej' else 'P-plads Vindingevej' end as busterminal,
eqo_in.export_value as in_transport, 
eqo_out.export_value as out_transport,
er.transport_in_from_id, er.transport_out_to_id, 
case when er.arrival_time is not null and er.arrival_time > 0 then concat(TO_CHAR(floor(er.arrival_time), 'fm00'),':',TO_CHAR((er.arrival_time-floor(er.arrival_time))*60, 'fm00'))end as arrival_time, 
case when er.departure_time is not null and er.departure_time > 0 then concat(TO_CHAR(floor(er.departure_time), 'fm00'),':',TO_CHAR((er.departure_time-floor(er.departure_time))*60, 'fm00'))end as departure_time, 
er.arrival_flight, er.departure_flight,
COALESCE(cd.in_date, cdf.in_date) in_date, COALESCE(cd.out_date, cdf.out_date) as out_date
from event_registration er left outer join event_registration erm on erm.id = er.registration_master_id  
left outer join event_question_response eqr_in on eqr_in.event_registration_id = er.id and eqr_in.event_question_id = (CASE WHEN er.event_id = 9 then 35   WHEN er.event_id = 11 then 104 END)  and eqr_in.event_question_option_id is not null
left outer join event_question_option eqo_in on eqo_in.id = eqr_in.event_question_option_id
left outer join event_question_response eqr_out on eqr_out.event_registration_id = er.id and eqr_out.event_question_id = (CASE WHEN er.event_id = 9 then 40   WHEN er.event_id = 11 then 109 END) and eqr_out.event_question_option_id is not null
left outer join event_question_option eqo_out on eqo_out.id = eqr_out.event_question_option_id
left outer join (select eqr.event_registration_id, min(TO_DATE(eqo.export_value,'YYYY-MM-DD')) as in_date, max(TO_DATE(eqo.export_value,'YYYY-MM-DD')+1)as out_date from event_question_response eqr 
                           left join event_question_option eqo on eqo.id = eqr.event_question_option_id 
                           where eqr.event_question_id=36
                          group by eqr.event_registration_id ) cd on cd.event_registration_id = er.id
left outer join (select registration_id, min(TO_DATE(day,'YYYY_MM_DD'))as in_date , max(TO_DATE(day,'YYYY_MM_DD')+1) as out_date from event_registration_day where participation = 'volunteer' group by registration_id) cdf on cdf.registration_id= er.id
left outer join event_registration era on era.id = er.associated_group_id
left outer join "event_subcamp_area" sca on sca.id = COALESCE(erm.subcamp_area_id,er.subcamp_area_id,era.subcamp_area_id) 
where (er.event_id  = 9 or er.event_id = 11) and er.master = false and er.state = 'open' and COALESCE(erm.state,'open') = 'open'
)
