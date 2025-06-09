##################################################
## Project: RELN-NOTCH cross-talk in Lymphatics
## Script purpose: Finding drug targets in the RELN_NOTCH cross-talk map 
## Date: 12.03.2025
## Author: Luiz Ladeira
##################################################

library(httr)
library(dplyr)
library(purrr)
library(tidyr)
library(minervar)

if(packageVersion("minervar") < "0.8.3") {
  stop("Please install package:minervar 0.8.3")
}

remotes::install_gitlab(repo = "uniluxembourg/lcsb/BioCore/disease_maps/tmcuration", host = "gitlab.com", dependencies = TRUE)

#########
### Load the bioentities from the map
components <- minervar::get_map_components("https://ontox.elixir-luxembourg.org/minerva/api/", project_id = "RELN_NOTCH_LECs")
bioentities <- components$map_elements[[1]]

# Access data
map_ids <- as.character(586)
full_elements_list <- map_df(map_ids, ~components$map_elements[[.x]])

### To make a search loop for drugs using the map entities, let's create an API stub for this project
map_project <- paste0("https://ontox.elixir-luxembourg.org/minerva/api/projects/RELN_NOTCH_LECs/")

### Let's cycle through the aliases and fetch all drugs targeting the bioentities
all_drugs <- sapply(bioentities$id, 
                    function(x) fromJSON(ask_GET(paste0(map_project, "drugs:search?target=ALIAS:", x))))

# Flatten the nested lists into a dataframe
all_drugs_df <- map_df(all_drugs, ~ {
  # Convert each nested list into a dataframe
  as.data.frame(.x, stringsAsFactors = FALSE)
})

# Add a names_sep parameter to create unique column names
all_drugs_df <- all_drugs_df %>%
  unnest(cols = targets, names_sep = "_", keep_empty = TRUE) 

all_drugs_df <- all_drugs_df %>%
  unnest(cols = targets_targetParticipants, names_sep = "_", keep_empty = TRUE)

all_drugs_df <- all_drugs_df %>%
  unnest(cols = references, names_sep = "_", keep_empty = TRUE)

# Remove column references. We will not use it, and it is a nested list.
all_drugs_df <- all_drugs_df %>% select(-last_col())
      
# Save the fully unnested dataframe
write.table(all_drugs_df, file = "drugs_RELN_NOTCH_from_map.tsv", sep = "\t", row.names = FALSE, quote = TRUE)
