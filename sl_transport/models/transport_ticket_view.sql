CREATE OR REPLACE VIEW transport_ticket_view AS (
select row_number() over () as id, t.* from (select tt.name, tt.ticket_type, registration_id  , tt.webtour_tour_id, wt.from_rp_id,wt.to_rp_id, wt.webtour_etd as etd, webtour_eta as eta,wt.note as note, 1 as pax , 'reg' as source from transport_ticket tt
inner join transport_webtourtour wt on wt.id = tt.webtour_tour_id
union
select '' as name, tt.ticket_type, er.registration_master_id , tt.webtour_tour_id, wt.from_rp_id,wt.to_rp_id, wt.webtour_etd as etd, webtour_eta as eta, wt.note as note, count(tt.id)  as pax , 'sum' as source from transport_ticket tt
inner join event_registration er on er.id = tt.registration_id
inner join transport_webtourtour wt on wt.id = tt.webtour_tour_id
where er.registration_master_id is not Null
group by 1,2,3,4,5,6,7,8,9) t
)
