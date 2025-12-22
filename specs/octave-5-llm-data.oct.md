===OCTAVE_DATA===
META:
  TYPE::LLM_PROFILE
  VERSION::"5.1.0"
  STATUS::APPROVED
  TOKENS::"~75"
  REQUIRES::octave-5-llm-core
  PURPOSE::compression_and_instances

---

// OCTAVE DATA: Rules for compressing prose and writing instances. Inject WITH core.

§1::DATA_MODE
PATTERN::KEY::value[L1_simple_assignment]
LEVELS::L1∨L2[never_L3_L4]
BRACKETS::lists∨inline_maps[never_holographic]
FORBIDDEN::["example"∧CONSTRAINT→§TARGET][use_schema_mode]

§2::COMPRESSION
PRESERVE::[
  numbers[exact],
  names[identifiers,proper_nouns],
  codes[error_codes,IDs,hashes],
  operators[all_OCTAVE_symbols],
  §anchors[targets,sections],
  "quoted"[verbatim_definitions]
]

DROP::[the,a,an,of,for,to,with,that,which,basically,essentially,simply]

REWRITE::verbose_phrase→minimal_token[preserve_meaning]

§3::ABBREVIATIONS
STATUS::[DONE,WIP,PENDING,BLOCKED,OPEN,CLOSED]
COMMON::[impl,config,env,auth,db,msg,req,res,fn,var,val]
CUSTOM::define_in_document_if_domain_specific

§4::LIST_FORMS
ALTERNATIVES::a∨b∨c[choose_one]
COLLECTION::[a,b,c][all_members]
SEQUENCE::[A→B→C][ordered_steps]
CONCAT::a⧺b⧺c[mechanical_join]
INLINE_MAP::[key::val,key2::val2][dense_key_value_pairs]
EMPTY::[][explicit_empty_state]

§5::ANCHORS
RULE::compress_around_anchors[never_rewrite_anchors]
VERBATIM::[code_blocks,example_strings,"quoted_canonical",numbers,enums]
BOUNDARIES::preserve_distinctions[A⇌B_must_remain_distinct]

§6::FORBIDDEN_REWRITES
NEVER::[
  introduce_absolutes[always,never,must][unless_in_source],
  collapse_boundaries[merge_distinct_concepts],
  strengthen_claims[change_hedging],
  drop_numbers[exact_values_required],
  rewrite_code[verbatim_only]
]

§7::REFERENCE
EXAMPLES::see_core.§7.DATA_PATTERN

===END===
