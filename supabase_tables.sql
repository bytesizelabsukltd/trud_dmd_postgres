-- f_lookup_AvailRestrictInfoType
-- cd|desc
-- availabilityrestriction

CREATE TABLE lookup_availabilityrestriction (
    cd VARCHAR(60) PRIMARY KEY,  
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_BasisOfNameInfoType
-- cd|desc
-- basisofname

CREATE TABLE lookup_basisofname (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(150) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_BasisOfStrengthInfoType
-- cd|desc
-- basisofstrnth

CREATE TABLE lookup_basisofstrnth (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(150) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_ColourInfoType
-- cd|desc
-- colour

CREATE TABLE lookup_colour (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_CombPackIndInfoType
-- cd|desc
-- combinationpackind

CREATE TABLE lookup_combinationpackind (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_CombProdIndInfoType
-- cd|desc
-- combinationprodind

CREATE TABLE lookup_combinationprodind (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_ControlDrugCatInfoType
-- cd|desc
-- controldrugcategory 

CREATE TABLE lookup_controldrugcategory (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_DfIndInfoType
-- cd|desc
-- dfindicator

CREATE TABLE lookup_dfindicator (
    cd VARCHAR(60) PRIMARY KEY,  
    descr VARCHAR(20) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_DiscIndInfoType
-- cd|desc
-- discontinuedind

CREATE TABLE lookup_discontinuedind (
    cd VARCHAR(60) PRIMARY KEY,  
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_DNDInfoType
-- cd|desc
-- dnd

CREATE TABLE lookup_dnd (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_DtPayCatInfoType
-- cd|desc
-- dtpaymentcategory

CREATE TABLE lookup_dtpaymentcategory (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_FlavourInfoType
-- cd|desc
-- flavour

CREATE TABLE lookup_flavour (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_FormHistoryInfoType
-- cd|cddt|cdprev|desc
-- form

CREATE TABLE lookup_form (
    cd BIGINT PRIMARY KEY, 
    cddt DATE NULL, 
    cdprev BIGINT NULL, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_LegalCatInfoType
-- cd|desc
-- legalcategory

CREATE TABLE lookup_legalcategory (
    cd VARCHAR(60) PRIMARY KEY,  
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_LicAuthChgRsnInfoType
-- cd|desc
-- licensingauthoritychangereason

CREATE TABLE lookup_licensingauthoritychangereason (
    cd VARCHAR(60) PRIMARY KEY,  
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_LicAuthIndInfoType
-- cd|desc
-- licensingauthority

CREATE TABLE lookup_licensingauthority (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_NamechangeReasonInfoType
-- cd|desc
-- namechangereason

CREATE TABLE lookup_namechangereason (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(150) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_OntFormRouteInfoType
-- cd|desc
-- ontformroute

CREATE TABLE lookup_ontformroute (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_PriceBasisInfoType
-- cd|desc
-- pricebasis

CREATE TABLE lookup_pricebasis (
    cd VARCHAR(60) PRIMARY KEY,  
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_ReimbStatInfoType
-- cd|desc
-- reimbursementstatus

CREATE TABLE lookup_reimbursementstatus (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_RouteHistoryInfoType
-- cd|cddt|cdprev|desc
-- route

CREATE TABLE lookup_route (
    cd BIGINT PRIMARY KEY, 
    cddt DATE NULL, 
    cdprev BIGINT NULL, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_SpecContInfoType
-- cd|desc
-- speccont

CREATE TABLE lookup_speccont (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_SupplierSupplierInfoType
-- cd|cddt|cdprev|invalid|desc
-- supplier
-- null-values: invalid

CREATE TABLE lookup_supplier (
    cd BIGINT PRIMARY KEY, 
    cddt DATE NULL, 
    cdprev BIGINT NULL, 
    invalid BOOLEAN NOT NULL, 
    descr VARCHAR(80) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_UoMHistoryInfoType
-- cd|cddt|cdprev|desc
-- unitofmeasure

CREATE TABLE lookup_unitofmeasure (
    cd BIGINT PRIMARY KEY, 
    cddt DATE NULL, 
    cdprev BIGINT NULL, 
    descr VARCHAR(150) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_VirProdNoAvailInfoType
-- cd|desc
-- virtualproductnonavail

CREATE TABLE lookup_virtualproductnonavail (
    cd VARCHAR(60) PRIMARY KEY,  
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_lookup_VirProdPresStatInfoType
-- cd|desc
-- virtualproductpresstatus

CREATE TABLE lookup_virtualproductpresstatus (
    cd VARCHAR(60) PRIMARY KEY, 
    descr VARCHAR(60) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_ingredient
-- isid|isiddt|isidprev|invalid|nm
-- ing
-- null-values: invalid

CREATE TABLE ingredient (
    isid BIGINT PRIMARY KEY, 
    isiddt DATE NULL, 
    isidprev BIGINT NULL, 
    invalid BOOLEAN NOT NULL, 
    nm VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vtm
-- vtmid|invalid|nm|abbrevnm|vtmidprev|vtmiddt
-- vtm
-- null-values: invalid

CREATE TABLE vtm (
    vtmid BIGINT PRIMARY KEY, 
    invalid BOOLEAN NOT NULL, 
    nm VARCHAR(255) NOT NULL, 
    abbrevnm VARCHAR(60) NULL, 
    vtmidprev BIGINT NULL, 
    vtmiddt DATE NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmp_VmpType
-- vpid|vpiddt|vpidprev|vtmid|invalid|nm|abbrevnm|basiscd|nmdt|nmprev|basis_prevcd|nmchangecd|combprodcd|pres_statcd|sug_f|glu_f|pres_f|cfc_f|non_availcd|non_availdt|df_indcd|udfs|udfs_uomcd|unit_dose_uomcd|bnf_code
-- vmp
-- added: bnf_code
-- null-values: invalid,sug_f,glu_f,pres_f,cfc_f

CREATE TABLE vmp (
    id SERIAL PRIMARY KEY,
    vpid BIGINT NOT NULL, 
    vpiddt DATE NULL, 
    vpidprev BIGINT NULL, 
    vtmid BIGINT NULL REFERENCES vtm(vtmid) ON DELETE CASCADE, 
    invalid BOOLEAN NOT NULL, 
    nm VARCHAR(255) NOT NULL, 
    abbrevnm VARCHAR(60) NULL, 
    basiscd VARCHAR(60) NOT NULL REFERENCES lookup_basisofname(cd) ON DELETE CASCADE, 
    nmdt DATE NULL, 
    nmprev VARCHAR(255) NULL, 
    basis_prevcd VARCHAR(60) NULL REFERENCES lookup_basisofname(cd) ON DELETE CASCADE, 
    nmchangecd VARCHAR(60) NULL REFERENCES lookup_namechangereason(cd) ON DELETE CASCADE, 
    combprodcd VARCHAR(60) NULL REFERENCES lookup_combinationprodind(cd) ON DELETE CASCADE, 
    pres_statcd VARCHAR(60) NOT NULL REFERENCES lookup_virtualproductpresstatus(cd) ON DELETE CASCADE, 
    sug_f BOOLEAN NOT NULL, 
    glu_f BOOLEAN NOT NULL, 
    pres_f BOOLEAN NOT NULL, 
    cfc_f BOOLEAN NOT NULL, 
    non_availcd VARCHAR(60) NULL REFERENCES lookup_virtualproductnonavail(cd) ON DELETE CASCADE, 
    non_availdt DATE NULL, 
    df_indcd VARCHAR(60) NOT NULL REFERENCES lookup_dfindicator(cd) ON DELETE CASCADE, 
    udfs DECIMAL(10,3) NULL, 
    udfs_uomcd BIGINT NULL REFERENCES lookup_unitofmeasure(cd) ON DELETE CASCADE, 
    unit_dose_uomcd BIGINT NULL REFERENCES lookup_unitofmeasure(cd) ON DELETE CASCADE, 
    bnf_code VARCHAR(15) NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmp_VpiType
-- vpid|isid|basis_strntcd|bs_subid|strnt_nmrtr_val|strnt_nmrtr_uomcd|strnt_dnmtr_val|strnt_dnmtr_uomcd
-- vpi

CREATE TABLE vmp_vpi (
    id SERIAL PRIMARY KEY,
    vpid INT NOT NULL REFERENCES vmp(id) ON DELETE CASCADE,
    isid BIGINT NOT NULL REFERENCES ingredient(isid) ON DELETE CASCADE, 
    basis_strntcd VARCHAR(60) NULL REFERENCES lookup_basisofstrnth(cd) ON DELETE CASCADE, 
    bs_subid BIGINT NULL REFERENCES ingredient(isid) ON DELETE CASCADE, 
    strnt_nmrtr_val DECIMAL(10,3) NULL, 
    strnt_nmrtr_uomcd BIGINT NULL REFERENCES lookup_unitofmeasure(cd) ON DELETE CASCADE, 
    strnt_dnmtr_val DECIMAL(10,3) NULL, 
    strnt_dnmtr_uomcd BIGINT NULL REFERENCES lookup_unitofmeasure(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmp_ControlInfoType
-- vpid|catcd|catdt|cat_prevcd
-- controlinfo

CREATE TABLE vmp_controlinfo (
    id SERIAL PRIMARY KEY,
    vpid INT NOT NULL REFERENCES vmp(id) ON DELETE CASCADE, 
    catcd VARCHAR(60) NOT NULL REFERENCES lookup_controldrugcategory(cd) ON DELETE CASCADE, 
    catdt DATE NULL, 
    cat_prevcd VARCHAR(60) NULL REFERENCES lookup_controldrugcategory(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmp_DrugFormType
-- vpid|formcd
-- dform

CREATE TABLE vmp_dform (
    id SERIAL PRIMARY KEY,
    vpid INT NOT NULL REFERENCES vmp(id) ON DELETE CASCADE, 
    formcd BIGINT NOT NULL REFERENCES lookup_form(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmp_DrugRouteType
-- vpid|routecd
-- droute

CREATE TABLE vmp_droute (
    id SERIAL PRIMARY KEY,
    vpid INT NOT NULL REFERENCES vmp(id) ON DELETE CASCADE, 
    routecd BIGINT NOT NULL REFERENCES lookup_route(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmp_OntDrugFormType
-- vpid|formcd
-- ont

CREATE TABLE vmp_ont (
    id SERIAL PRIMARY KEY,
    vpid INT NOT NULL REFERENCES vmp(id) ON DELETE CASCADE, 
    formcd VARCHAR(60) NOT NULL REFERENCES lookup_ontformroute(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmpp_VmppType
-- vppid|invalid|nm|abbrevnm|vpid|qtval|qty_uomcd|combpackcd
-- vmpp
-- missing: abbrevnm
-- changed: qtyval-qtval
-- added: bnf_code,abbrevnm
-- null-values: invalid

CREATE TABLE vmpp (
    id SERIAL PRIMARY KEY,
    vppid BIGINT NOT NULL, 
    invalid BOOLEAN NOT NULL, 
    nm VARCHAR(420) NOT NULL,
    abbrevnm VARCHAR(60) NULL,  
    vpid INT NOT NULL REFERENCES vmp(id) ON DELETE CASCADE, 
    qtval DECIMAL(10,2) NULL, 
    qty_uomcd BIGINT NULL REFERENCES lookup_unitofmeasure(cd) ON DELETE CASCADE, 
    combpackcd VARCHAR(60) NULL REFERENCES lookup_combinationpackind(cd) ON DELETE CASCADE, 
    bnf_code VARCHAR(15) NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmpp_ContentType
-- prntvppid|childvppid
-- vmpp_contenttype

CREATE TABLE vmpp_contenttype (
    id SERIAL PRIMARY KEY,
    prntvppid INT NOT NULL REFERENCES vmpp(id) ON DELETE CASCADE,
    childvppid INT NOT NULL REFERENCES vmpp(id) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_vmpp_DtInfoType
-- vppid|pay_catcd|price|dt|prevprice
-- dtinfo

CREATE TABLE vmpp_dtinfo (
    id SERIAL PRIMARY KEY,
    vppid INT NOT NULL REFERENCES vmpp(id) ON DELETE CASCADE, 
    pay_catcd VARCHAR(60) NOT NULL REFERENCES lookup_dtpaymentcategory(cd) ON DELETE CASCADE, 
    price INTEGER NULL, 
    dt DATE NULL, 
    prevprice INTEGER NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_amp_AmpType
-- apid|invalid|vpid|nm|abbrevnm|desc|nmdt|nm_prev|suppcd|lic_authcd|lic_auth_prevcd|lic_authchangecd|lic_authchangedt|combprodcd|flavourcd|ema|parallel_import|avail_restrictcd|bnf_code
-- amp
-- added: bnf_code
-- null-values: invalid,ema,parallel_import

CREATE TABLE amp (
    id SERIAL PRIMARY KEY,
    apid BIGINT NOT NULL, 
    invalid BOOLEAN NOT NULL, 
    vpid INT NOT NULL REFERENCES vmp(id) ON DELETE CASCADE, 
    nm VARCHAR(255) NOT NULL, 
    abbrevnm VARCHAR(60) NULL, 
    descr VARCHAR(700) NOT NULL, 
    nmdt DATE NULL, 
    nm_prev VARCHAR(255) NULL, 
    suppcd BIGINT NOT NULL REFERENCES lookup_supplier(cd) ON DELETE CASCADE, 
    lic_authcd VARCHAR(60) NOT NULL REFERENCES lookup_licensingauthority(cd) ON DELETE CASCADE, 
    lic_auth_prevcd VARCHAR(60) NULL REFERENCES lookup_licensingauthority(cd) ON DELETE CASCADE, 
    lic_authchangecd VARCHAR(60) NULL REFERENCES lookup_licensingauthoritychangereason(cd) ON DELETE CASCADE, 
    lic_authchangedt DATE NULL, 
    combprodcd VARCHAR(60) NULL REFERENCES lookup_combinationprodind(cd) ON DELETE CASCADE, 
    flavourcd VARCHAR(60) NULL REFERENCES lookup_flavour(cd) ON DELETE CASCADE, 
    ema BOOLEAN NOT NULL, 
    parallel_import BOOLEAN NOT NULL, 
    avail_restrictcd VARCHAR(60) NOT NULL REFERENCES lookup_availabilityrestriction(cd) ON DELETE CASCADE, 
    bnf_code VARCHAR(15) NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_amp_ApiType
-- apid|isid|strnth|uomcd
-- aping

CREATE TABLE amp_ingredient (
    id SERIAL PRIMARY KEY,
    apid INT NOT NULL REFERENCES amp(id) ON DELETE CASCADE,
    isid BIGINT NOT NULL REFERENCES ingredient(isid) ON DELETE CASCADE,
    strnth DECIMAL(10,3) NULL,
    uomcd BIGINT NOT NULL REFERENCES lookup_unitofmeasure(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_amp_AppProdInfoType
-- apid|sz_weight|colourcd|prod_order_no
-- apinfo

CREATE TABLE amp_apinfo (
    id SERIAL PRIMARY KEY,
    apid INT NOT NULL REFERENCES amp(id) ON DELETE CASCADE,
    sz_weight VARCHAR(100) NULL,
    colourcd VARCHAR(60) NULL REFERENCES lookup_colour(cd) ON DELETE CASCADE,
    prod_order_no VARCHAR(20) NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_amp_LicRouteType
-- apid|routecd
-- licroute

CREATE TABLE amp_licroute (
    id SERIAL PRIMARY KEY,
    apid INT NOT NULL REFERENCES amp(id) ON DELETE CASCADE,
    routecd BIGINT NOT NULL REFERENCES lookup_route(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_ampp_AmppType
-- appid|invalid|nm|abbrevnm|vppid|apid|combpackcd|legal_catcd|subp|disccd|discdt
-- ampp
-- null-values: invalid
-- added: bnf_code

CREATE TABLE ampp (
    id SERIAL PRIMARY KEY,
    appid BIGINT NOT NULL, 
    invalid BOOLEAN NOT NULL, 
    nm VARCHAR(774) NOT NULL, 
    abbrevnm VARCHAR(60) NULL, 
    vppid INT NOT NULL REFERENCES vmpp(id) ON DELETE CASCADE, 
    apid INT NOT NULL REFERENCES amp(id) ON DELETE CASCADE, 
    combpackcd VARCHAR(60) NULL REFERENCES lookup_combinationpackind(cd) ON DELETE CASCADE, 
    legal_catcd VARCHAR(60) NOT NULL REFERENCES lookup_legalcategory(cd) ON DELETE CASCADE, 
    subp VARCHAR(30) NULL, 
    disccd VARCHAR(60) NULL REFERENCES lookup_discontinuedind(cd) ON DELETE CASCADE, 
    discdt DATE NULL, 
    bnf_code VARCHAR(15) NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_ampp_ContentType
-- prntappid|childappid
-- ampp_contenttype

CREATE TABLE ampp_contenttype (
    id SERIAL PRIMARY KEY,
    prntappid INT NOT NULL REFERENCES ampp(id) ON DELETE CASCADE,
    childappid INT NOT NULL REFERENCES ampp(id) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_ampp_PackInfoType
-- appid|reimb_statcd|reimb_statdt|reimb_statprevcd|pack_order_no
-- packinfo

CREATE TABLE ampp_packinfo (
    id SERIAL PRIMARY KEY,
    appid INT NOT NULL REFERENCES ampp(id) ON DELETE CASCADE, 
    reimb_statcd VARCHAR(60) NOT NULL REFERENCES lookup_reimbursementstatus(cd) ON DELETE CASCADE, 
    reimb_statdt DATE NULL, 
    reimb_statprevcd VARCHAR(60) NULL REFERENCES lookup_reimbursementstatus(cd) ON DELETE CASCADE, 
    pack_order_no VARCHAR(20) NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_ampp_PrescInfoType
-- appid|sched_2|acbs|padm|fp10_mda|sched_1|hosp|nurse_f|enurse_f|dent_f
-- prescribinfo
-- null-values: sched_2,acbs,padm,fp10_mda,sched_1,hosp,nurse_f,enurse_f,dent_f

CREATE TABLE ampp_prescribinfo (
    id SERIAL PRIMARY KEY,
    appid INT NOT NULL REFERENCES ampp(id) ON DELETE CASCADE,
    sched_2 BOOLEAN NOT NULL,
    acbs BOOLEAN NOT NULL,
    padm BOOLEAN NOT NULL,
    fp10_mda BOOLEAN NOT NULL,
    sched_1 BOOLEAN NOT NULL,
    hosp BOOLEAN NOT NULL,
    nurse_f BOOLEAN NOT NULL,
    enurse_f BOOLEAN NOT NULL,
    dent_f BOOLEAN NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_ampp_PriceInfoType
-- appid|price|pricedt|price_prev|price_basiscd
-- priceinfo

CREATE TABLE ampp_priceinfo (
    id SERIAL PRIMARY KEY,
    appid INT NOT NULL REFERENCES ampp(id) ON DELETE CASCADE,
    price INTEGER NULL,
    pricedt DATE NULL,
    price_prev INTEGER NULL,
    price_basiscd VARCHAR(60) NOT NULL REFERENCES lookup_pricebasis(cd) ON DELETE CASCADE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_ampp_ReimbInfoType
-- appid|px_chrgs|disp_fees|bb|cal_pack|spec_contcd|dndcd|fp34d
-- reimbinfo
-- null-values: bb,fp34d

CREATE TABLE ampp_reimbinfo (
    id SERIAL PRIMARY KEY,
    appid INT NOT NULL REFERENCES ampp(id) ON DELETE CASCADE,
    px_chrgs INTEGER NULL,
    disp_fees INTEGER NULL,
    bb BOOLEAN NOT NULL,
    ltd_stab BOOLEAN NULL,
    cal_pack BOOLEAN NOT NULL,
    spec_contcd VARCHAR(60) NULL REFERENCES lookup_speccont(cd) ON DELETE CASCADE,
    dndcd VARCHAR(60) NULL REFERENCES lookup_dnd(cd) ON DELETE CASCADE,
    fp34d BOOLEAN NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- f_gtin
-- amppid|gtin|startdt|enddt
-- gtin

CREATE TABLE gtin (
    id SERIAL PRIMARY KEY,
    amppid INT NOT NULL REFERENCES ampp(id) ON DELETE CASCADE, 
    gtin BIGINT NOT NULL, 
    startdt DATE NOT NULL, 
    enddt DATE NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE ingredient IS 'Ingredient';
COMMENT ON TABLE vtm IS 'Virtual Therapeutic Moiety';
COMMENT ON TABLE vmp IS 'Virtual Medicinal Product';
COMMENT ON TABLE vmp_vpi IS 'Virtual Product Ingredient';
COMMENT ON TABLE vmp_controlinfo IS 'Controlled Drug Prescribing Information';
COMMENT ON TABLE vmp_dform IS 'Dose Form';
COMMENT ON TABLE vmp_droute IS 'Drug Route';
COMMENT ON TABLE vmp_ont IS 'Ontology Drug Form & Route';
COMMENT ON TABLE vmpp IS 'Virtual Medicinal Product Pack';
COMMENT ON TABLE vmpp_contenttype IS 'Virtual Medicinal Product Pack Parent/Child Packs';
COMMENT ON TABLE vmpp_dtinfo IS 'Drug Tariff Category Information';
COMMENT ON TABLE amp IS 'Actual Medicinal Product';
COMMENT ON TABLE amp_ingredient IS 'Excipients';
COMMENT ON TABLE amp_apinfo IS 'Appliance Product Information';
COMMENT ON TABLE amp_licroute IS 'Licensed Route';
COMMENT ON TABLE ampp IS 'Actual Medicinal Product Pack';
COMMENT ON TABLE ampp_contenttype IS 'Actual Medicinal Product Pack Parent/Child Packs';
COMMENT ON TABLE ampp_packinfo IS 'Appliance Pack Information';
COMMENT ON TABLE ampp_prescribinfo IS 'Product Prescribing Information';
COMMENT ON TABLE ampp_priceinfo IS 'Medicinal Product Price';
COMMENT ON TABLE ampp_reimbinfo IS 'Reimbursement Information';
COMMENT ON TABLE gtin IS 'Global Trade Item Number';