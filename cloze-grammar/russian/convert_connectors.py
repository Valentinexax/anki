# Run BEFORE importing russian_grammar_cloze.txt, and only if the old Russian deck is already
# in your collection. Paste into Anki's Debug Console (Tools > Debug Console, or Ctrl+Shift+;)
# and press Ctrl+Enter.
# The old deck's 335 Supplement notes use a note type called "connectors"; the rebuilt file puts
# every note on "Typecloze", and Anki skips (as "conflicting") any note whose type differs.
# This converts those notes to Typecloze, field by field in order. Note IDs, GUIDs and review
# history are kept. Only notes whose 8th field (Sort ID) starts with RU- are touched.
# Changing note type is a schema change: Anki will ask for a one-way full sync afterwards.
old = mw.col.models.by_name("connectors")
new = mw.col.models.by_name("Typecloze")
if not old or not new:
    print("nothing to do: note type 'connectors' or 'Typecloze' not found")
else:
    nids = [nid for nid in mw.col.find_notes('"note:connectors"')
            if mw.col.get_note(nid).fields[7].startswith("RU-")]
    if not nids:
        print("nothing to do: no Russian notes use 'connectors'")
    else:
        assert len(old["flds"]) == len(new["flds"]), "field counts differ; use Browse > Change Note Type"
        info = mw.col.models.change_notetype_info(old_notetype_id=old["id"], new_notetype_id=new["id"])
        req = info.input
        req.note_ids.extend(nids)
        del req.new_fields[:]
        req.new_fields.extend(range(len(new["flds"])))
        mw.col.models.change_notetype_of_notes(req)
        try:
            mw.reset()
        except Exception:
            pass
        print(f"converted {len(nids)} notes from 'connectors' to 'Typecloze'")
