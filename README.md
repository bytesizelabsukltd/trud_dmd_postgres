# DM+d Supabase Implementation

The Dictionary of Medicines and Devices (DM+D) is a comprehensive dataset encompassing all medicines and devices utilized within the UK National Health Service (NHS). This dataset is jointly maintained by the NHS Business Services Authority and NHS Digital, and is provided in XML format under an Open Government License.
This repository forms the initial component of a larger application, focusing on creating a Supabase (PostgreSQL) implementation of the DM+D. The project utilises Python to parse the complete DM+D XML files, converting them into CSV format and upload them to supabase. During this process, each entry is assigned a unique identifier before being uploaded to Supabase.


The project is still in development, with ongoing work to integrate additional data sources. These include the electronic Medicines Compendium (eMC), the British National Formulary (BNF), and Counter Intelligence Plus (CIPlus). A key challenge being addressed is the integration of this data, as there isn't a straightforward mapping method available. The ultimate goal is to create comprehensive, interlinked records that combine data from all these sources.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file (create this in the root directory).

Follow this guide to get your TRUD API Key: https://isd.digital.nhs.uk/trud/users/guest/filters/0/api

Leave the BASE_DIR the same.

Example .env file:

```
TRUD_API_KEY=XXXXXXXXX
BASE_DIR=PIPELINE_DATA_BASEDIR/dmd/
SUPABASE_URL=https://XXXXXXXXX.supabase.co
SUPABASE_KEY=XXXXXXXXX
SUPABASE_SERVICE_KEY=XXXXXXXXX
```
## Installation Requirements
Packages like os, datetime, csv, time, json, re, and pathlib are part of Python's standard library and don't require separate installation.

```bash
pip install python-dotenv
pip install supabase
pip install lxml
pip install colorama
```
## Deployment

Before you deploy, go to your supabase database instance, and create this Postgres Database function using the built-in SQL Editor in Supabase. This is to allow us to insert SQL over the Supabase API.

```SQL
CREATE OR REPLACE FUNCTION execute_sql(sql text)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  EXECUTE sql;
END;
$$;
```

Create this function too, which allows us to delete the tables via API. When importing the data, we first delete all existing instances, because the IDs of some SNOMED objects can change. And since the data model contains foreign key constraints, the order we delete the files is significant.

```SQL
CREATE OR REPLACE FUNCTION public."deleteDMDData"()
RETURNS void AS $$
BEGIN
    -- Use TRUNCATE instead of DELETE for faster operation and to reset sequences
    TRUNCATE TABLE public.gtin CASCADE;
    TRUNCATE TABLE public.ampp_contenttype CASCADE;
    TRUNCATE TABLE public.ampp_packinfo CASCADE;
    TRUNCATE TABLE public.ampp_prescribinfo CASCADE;
    TRUNCATE TABLE public.ampp_priceinfo CASCADE;
    TRUNCATE TABLE public.ampp_reimbinfo CASCADE;
    TRUNCATE TABLE public.ampp CASCADE;
    TRUNCATE TABLE public.amp_apinfo CASCADE;
    TRUNCATE TABLE public.amp_ingredient CASCADE;
    TRUNCATE TABLE public.amp_licroute CASCADE;
    TRUNCATE TABLE public.amp CASCADE;
    TRUNCATE TABLE public.vmpp_contenttype CASCADE;
    TRUNCATE TABLE public.vmpp_dtinfo CASCADE;
    TRUNCATE TABLE public.vmpp CASCADE;
    TRUNCATE TABLE public.vmp_controlinfo CASCADE;
    TRUNCATE TABLE public.vmp_dform CASCADE;
    TRUNCATE TABLE public.vmp_droute CASCADE;
    TRUNCATE TABLE public.vmp_ont CASCADE;
    TRUNCATE TABLE public.vmp_vpi CASCADE;
    TRUNCATE TABLE public.vmp CASCADE;
    TRUNCATE TABLE public.vtm CASCADE;
    TRUNCATE TABLE public.ingredient CASCADE;
    TRUNCATE TABLE public.lookup_availabilityrestriction CASCADE;
    TRUNCATE TABLE public.lookup_basisofname CASCADE;
    TRUNCATE TABLE public.lookup_basisofstrnth CASCADE;
    TRUNCATE TABLE public.lookup_colour CASCADE;
    TRUNCATE TABLE public.lookup_combinationpackind CASCADE;
    TRUNCATE TABLE public.lookup_combinationprodind CASCADE;
    TRUNCATE TABLE public.lookup_controldrugcategory CASCADE;
    TRUNCATE TABLE public.lookup_dfindicator CASCADE;
    TRUNCATE TABLE public.lookup_discontinuedind CASCADE;
    TRUNCATE TABLE public.lookup_dnd CASCADE;
    TRUNCATE TABLE public.lookup_dtpaymentcategory CASCADE;
    TRUNCATE TABLE public.lookup_flavour CASCADE;
    TRUNCATE TABLE public.lookup_form CASCADE;
    TRUNCATE TABLE public.lookup_legalcategory CASCADE;
    TRUNCATE TABLE public.lookup_licensingauthority CASCADE;
    TRUNCATE TABLE public.lookup_licensingauthoritychangereason CASCADE;
    TRUNCATE TABLE public.lookup_namechangereason CASCADE;
    TRUNCATE TABLE public.lookup_ontformroute CASCADE;
    TRUNCATE TABLE public.lookup_pricebasis CASCADE;
    TRUNCATE TABLE public.lookup_reimbursementstatus CASCADE;
    TRUNCATE TABLE public.lookup_route CASCADE;
    TRUNCATE TABLE public.lookup_speccont CASCADE;
    TRUNCATE TABLE public.lookup_supplier CASCADE;
    TRUNCATE TABLE public.lookup_unitofmeasure CASCADE;
    TRUNCATE TABLE public.lookup_virtualproductnonavail CASCADE;
    TRUNCATE TABLE public.lookup_virtualproductpresstatus CASCADE;
END;
$$ LANGUAGE plpgsql;
```

After that's done, run the pipeline using: 

```bash
python run.py
```

This will create the database tables in supabase, download the latest DM+d release, unpack the xml files, and run a series of operations to parse the data and then finally upload it to supabase. 
## Post Deployment

After that, we can deploy Postgres fatabase functions to query the data. These functions live inside your database, and they can be used with the API.

### To Search for VTM

```SQL
CREATE OR REPLACE FUNCTION public."searchVtmByNameOrVtmid"(search_term text) 
RETURNS json AS $$
DECLARE
    result json;
    result_count integer;
BEGIN
    WITH search_results AS (
        SELECT vtm.vtmid, vtm.nm
        FROM vtm
        WHERE (vtm.vtmid::text = search_term OR vtm.nm ILIKE '%' || search_term || '%')
          AND vtm.invalid = FALSE
        ORDER BY vtm.nm ASC
    )
    SELECT json_build_object(
        'count', (SELECT COUNT(*) FROM search_results),
        'results', COALESCE(json_agg(
            json_build_object(
                'vtmid', sr.vtmid,
                'nm', sr.nm
            )
        ), '[]'::json)
    )
    INTO result
    FROM search_results sr;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### To Search for VMP

```SQL
CREATE OR REPLACE FUNCTION public."searchVmpByNameOrVpid"(search_term text) 
RETURNS json AS $$
DECLARE
    result json;
    result_count integer;
BEGIN
    WITH search_results AS (
        SELECT vmp.id, vmp.vpid, vmp.nm
        FROM vmp
        WHERE (vmp.id::text = search_term 
               OR vmp.vpid::text = search_term 
               OR vmp.nm ILIKE '%' || search_term || '%')
          AND vmp.invalid = FALSE
        ORDER BY vmp.nm ASC
    )
    SELECT json_build_object(
        'count', (SELECT COUNT(*) FROM search_results),
        'results', COALESCE(json_agg(
            json_build_object(
                'id', sr.id,
                'vpid', sr.vpid,
                'nm', sr.nm
            )
        ), '[]'::json)
    )
    INTO result
    FROM search_results sr;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### To Search for VMPP

```SQL
CREATE OR REPLACE FUNCTION public."searchVmppByNameOrVppid"(search_term text) 
RETURNS json AS $$
DECLARE
    result json;
    result_count integer;
BEGIN
    WITH search_results AS (
        SELECT vmpp.id, vmpp.vppid, vmpp.nm
        FROM vmpp
        WHERE (vmpp.id::text = search_term 
               OR vmpp.vppid::text = search_term 
               OR vmpp.nm ILIKE '%' || search_term || '%')
          AND vmpp.invalid = FALSE
        ORDER BY vmpp.nm ASC
    )
    SELECT json_build_object(
        'count', (SELECT COUNT(*) FROM search_results),
        'results', COALESCE(json_agg(
            json_build_object(
                'id', sr.id,
                'vppid', sr.vppid,
                'nm', sr.nm
            )
        ), '[]'::json)
    )
    INTO result
    FROM search_results sr;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### To Search for AMP

```SQL
CREATE OR REPLACE FUNCTION public."searchAmpByNameOrApid"(search_term text) 
RETURNS json AS $$
DECLARE
    result json;
    result_count integer;
BEGIN
    WITH search_results AS (
        SELECT amp.id, amp.apid, amp.nm
        FROM amp
        WHERE (amp.id::text = search_term 
               OR amp.apid::text = search_term 
               OR amp.nm ILIKE '%' || search_term || '%')
          AND amp.invalid = FALSE
        ORDER BY amp.nm ASC
    )
    SELECT json_build_object(
        'count', (SELECT COUNT(*) FROM search_results),
        'results', COALESCE(json_agg(
            json_build_object(
                'id', sr.id,
                'apid', sr.apid,
                'nm', sr.nm
            )
        ), '[]'::json)
    )
    INTO result
    FROM search_results sr;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### To Search for AMPP

```SQL
CREATE OR REPLACE FUNCTION public."searchAmppByNameOrAppid"(search_term text) 
RETURNS json AS $$
DECLARE
    result json;
    result_count integer;
BEGIN
    WITH search_results AS (
        SELECT ampp.id, ampp.appid, ampp.nm
        FROM ampp
        WHERE (ampp.id::text = search_term 
               OR ampp.appid::text = search_term 
               OR ampp.nm ILIKE '%' || search_term || '%')
          AND ampp.invalid = FALSE
        ORDER BY ampp.nm ASC
    )
    SELECT json_build_object(
        'count', (SELECT COUNT(*) FROM search_results),
        'results', COALESCE(json_agg(
            json_build_object(
                'id', sr.id,
                'appid', sr.appid,
                'nm', sr.nm
            )
        ), '[]'::json)
    )
    INTO result
    FROM search_results sr;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

### To Search for GTIN

```SQL
CREATE OR REPLACE FUNCTION public."searchGtinByAppidOrGtinOrName"(search_term text)
RETURNS json AS $$
DECLARE
    result json;
BEGIN
    WITH search_results AS (
        SELECT 
            g.id,
            g.gtin,
            g.amppid,
            a.appid,
            a.nm
        FROM 
            gtin g
        JOIN 
            ampp a ON g.amppid = a.id
        WHERE 
            (a.appid::text = search_term 
            OR g.gtin::text = search_term
            OR a.nm ILIKE '%' || search_term || '%')
            AND (g.enddt IS NULL OR g.enddt >= CURRENT_DATE)
            AND a.invalid = FALSE
        ORDER BY 
            a.nm ASC, g.gtin ASC
    )
    SELECT json_build_object(
        'count', (SELECT COUNT(*) FROM search_results),
        'results', COALESCE(json_agg(
            json_build_object(
                'id', sr.id,
                'gtin', sr.gtin,
                'amppid', sr.amppid,
                'appid', sr.appid,
                'nm', sr.nm
            )
        ), '[]'::json)
    )
    INTO result
    FROM search_results sr;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```
## API Reference


The system includes API routes for retrieving various types of data, including:

Virtual Therapeutic Moiety (VTM)
Virtual Medicinal Product (VMP)
Virtual Medicinal Product Pack (VMPP)
Actual Medicinal Product (AMP)
Actual Medicinal Product Pack (AMPP)
Global Trade Identification Numbers (GTIN)

This implementation allows for efficient querying of drug data using GTINs, AMPP, AMP, VMPP, VMP, VTM.

#### Get VTM

```http
  /rest/v1/rpc/searchVtmByNameOrVtmid?search_term=paracetamol
```
#### Get VMP

```http
  /rest/v1/rpc/searchVmpByNameOrVpid?search_term=paracetamol
```
#### Get VMPP

```http
  /rest/v1/rpc/searchVmppByNameOrVppid?search_term=paracetamol
```
#### Get AMP

```http
  /rest/v1/rpc/searchAmpByNameOrApid?search_term=paracetamol
```
#### Get AMPP

```http
  /rest/v1/rpc/searchAmppByNameOrAppid?search_term=paracetamol
```
#### Get AMPP

```http
  /rest/v1/rpc/searchGtinByAppidOrGtinOrName?search_term=paracetamol
```

### Example Response

```json
  [
    {
      "searchGtinByAppidOrGtinOrName": {
        "count": 237,
        "results": [
          {
            "id": 17382,
            "gtin": 5000309007767,
            "amppid": 37404,
            "appid": 10667811000001104,
            "nm": "Anadin Paracetamol 500mg tablets (Haleon UK Trading Ltd) 12 tablet"
          },
          {
            "id": 759,
            "gtin": 5000309007774,
            "amppid": 1118,
            "appid": 1439611000001101,
            "nm": "Anadin Paracetamol 500mg tablets (Haleon UK Trading Ltd) 16 tablet"
          },
          {
            "id": 13667,
            "gtin": 5000347087509,
            "amppid": 27486,
            "appid": 7988111000001108,
            "nm": "Beechams Decongestant Plus with Paracetamol capsules (Haleon UK Trading Ltd) 16 capsule"
          },

    
        ]
      }
    }
  ]
```