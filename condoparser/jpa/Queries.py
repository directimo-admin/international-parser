GET_OFFERS_THAT_NO_LONGER_EXISTS_QUERY = "SELECT cnd.url as condo_url, cnd.name as condo_name, cnd.zone as condo_zone, off.* FROM `offer` as off " \
                                         "INNER JOIN `status` as sts on off.record_status_id = sts.id " \
                                         "LEFT JOIN `offer` as newOff on off.id = newOff.parent_id " \
                                         "INNER JOIN condo as cnd on cnd.id=off.condo_id " \
                                         "WHERE sts.name = 'EXISTING' AND newOff.id IS NULL "\
                                         "ORDER BY cnd.zone, cnd.name;"
GET_OFFERS_THAT_GOT_UPDATED = "SELECT cnd.url as condo_url, cnd.name as condo_name, cnd.zone as condo_zone," \
    "newOff.room_no AS new_room_no, newOff.bathroom_no AS new_bathroom_no, " \
    "newOff.construction_date AS new_construction_date, newOff.terase_usable_area AS new_terase_usable_area, " \
    "newOff.usable_area AS new_usable_area, newOff.current_price AS new_current_price, off.room_no AS old_room_no," \
    " off.bathroom_no AS old_bathroom_no, off.construction_date AS old_construction_date, " \
    "off.terase_usable_area AS old_terase_usable_area, off.usable_area AS old_usable_area, " \
    "off.current_price AS old_current_price, off.url AS url " \
    "FROM `offer` AS off " \
    "INNER JOIN `offer` AS newOff ON off.id = newOff.parent_id " \
    "INNER JOIN `status` AS stsOff ON off.record_status_id = stsOff.id " \
    "INNER JOIN condo as cnd on cnd.id=off.condo_id " \
    "INNER JOIN `status` AS stsNewOff ON newOff.record_status_id = stsNewOff.id " \
    "WHERE stsOff.name = 'EXISTING' AND stsNewOff.name = 'NEW' AND( NOT(off.room_no <=> newOff.room_no) OR NOT( off.bathroom_no <=> newOff.bathroom_no ) OR NOT( DATE(off.construction_date) <=> DATE(newOff.construction_date) ) OR NOT( off.terase_usable_area <=> newOff.terase_usable_area ) OR NOT( off.usable_area <=> newOff.usable_area ) OR NOT( off.current_price <=> newOff.current_price ) ) " \
    "ORDER BY cnd.zone, cnd.name;"

GET_NEW_OFFERS = "SELECT cnd.url as condo_url, cnd.name as condo_name, cnd.zone as condo_zone, off.* " \
                 "FROM offer  as off " \
                 "INNER JOIN status as sts on sts.id = off.record_status_id " \
                 "INNER JOIN condo as cnd on cnd.id=off.condo_id " \
                 "WHERE sts.name = 'NEW' AND off.parent_id IS NULL " \
                 "ORDER BY cnd.zone, cnd.name;"
