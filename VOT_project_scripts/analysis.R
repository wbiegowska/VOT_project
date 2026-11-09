# analysis.R  -  starter analysis for the Biegowska & Karamkesh project
# Uses the packages and functions shown in the course book
# (Al-Tamimi 2025, Statistics for Linguists using R): ch. 3.3 (lmer), ch. 7.4-7.5 (PCA, k-means),
# ch. 8.7 (cforest).
# Put this file in the same folder as tokens.txt, VQResults2.xls, w2v2_layers.csv and
# egemaps_tokens.csv, then run it chunk by chunk (select lines + Cmd/Ctrl+Enter in RStudio).

library(dplyr); library(readr); library(ggplot2); library(purrr)
library(lme4)        # mixed-effects models (book ch. 3.3)
library(FactoMineR)  # PCA (book ch. 7.4)
library(factoextra)  # PCA / cluster plots (book ch. 7.4-7.5)
library(party)       # Random Forests with conditional inference trees (book ch. 8.7)
library(pROC)        # ROC curves and AUC (book ch. 8)

# ---- 1. Read and merge -------------------------------------------------------
tok <- read_tsv("tokens.txt", na = c("--undefined--", ""),
                col_types = cols(sex = col_character())) %>%   # otherwise "F" is read as FALSE
  filter(clLabel != "CHECK_LABELS")
vq <- read_tsv("VQResults2.xls") %>%
  select(key = `File name`, hnr = hnrMeanFulldB, cpp = cppdB,
         tilt = tiltdB, hammarberg = hammarbergIndexdB)

bark <- function(f) 26.81 * f / (1960 + f) - 0.53     # Traunmueller (1990), in the course folder

dat <- tok %>%
  mutate(key = paste(file, word, sep = "_")) %>%
  left_join(vq, by = "key") %>%
  mutate(word    = tolower(word),
         voicing = factor(ifelse(word %in% c("bob", "big", "bags", "go"), "voiced", "voiceless")),
         place   = case_when(word %in% c("peas", "bob", "big", "bags") ~ "labial",
                             word == "toy" ~ "alveolar", TRUE ~ "velar"),
         group   = factor(group, levels = c("EN", "PL", "FA")),   # English = reference group
         f0rel   = 12 * log2(f0_10 / f0_50),                       # f0 at onset vs midpoint, semitones
         F1rel   = bark(F1_10) - bark(F1_50),                      # F1 at onset vs midpoint, Bark
         # closures marked "cl?" (unclear start) get no closure measures
         clDur_ms    = ifelse(clLabel == "cl?", NA, clDur_ms),
         voicingProp = ifelse(clLabel == "cl?", NA, voicingProp))

# ---- 2. Look at the data first ---------------------------------------------------
ggplot(dat, aes(group, VOT_ms, fill = voicing)) + geom_boxplot() + labs(y = "VOT (ms)")
ggplot(dat, aes(group, voicingProp, fill = voicing)) + geom_boxplot() +
  labs(y = "Proportion of voicing in closure")

# ---- 3. Mixed-effects models (book ch. 3.3) --------------------------------------
vl <- filter(dat, voicing == "voiceless")
m0 <- lmer(VOT_ms ~ 1     + (1 | file) + (1 | word), data = vl, REML = FALSE)
m1 <- lmer(VOT_ms ~ group + (1 | file) + (1 | word), data = vl, REML = FALSE)
anova(m0, m1)      # does knowing the group improve the model?
summary(m1)        # PL and FA estimates = difference from the English speakers, in ms

vd <- filter(dat, voicing == "voiced")
p0 <- lmer(voicingProp ~ 1     + (1 | file) + (1 | word), data = vd, REML = FALSE)
p1 <- lmer(voicingProp ~ group + (1 | file) + (1 | word), data = vd, REML = FALSE)
anova(p0, p1)
summary(p1)

# ---- 4. PCA and k-means (book ch. 7.4-7.5) ---------------------------------------
cues <- dat %>%
  select(group, voicing, VOT_ms, clDur_ms, voicingProp, f0rel, F1rel, hnr, cpp) %>%
  na.omit()
pca <- PCA(select(cues, -voicing), scale.unit = TRUE, ncp = 5, quali.sup = 1, graph = FALSE)
fviz_eig(pca)
fviz_pca_biplot(pca, habillage = cues$voicing, addEllipses = TRUE, repel = TRUE)
fviz_pca_ind(pca, habillage = cues$group, addEllipses = TRUE, label = "none")

set.seed(42)
scaled <- scale(select(cues, -group, -voicing))
km <- kmeans(scaled, centers = 2, nstart = 25)
table(cluster = km$cluster, voicing = cues$voicing, group = cues$group)
fviz_cluster(km, data = scaled, geom = "point")

# ---- 5. Random Forests per group: all cues vs VOT alone (book ch. 8.7) -----------
fit_rf <- function(d, f, mtry) {
  set.seed(42)
  m <- cforest(f, data = d, controls = cforest_unbiased(ntree = 500, mtry = mtry))
  pred <- predict(m, OOB = TRUE)
  list(model = m, accuracy = mean(pred == d$voicing),
       roc = roc(d$voicing, as.numeric(pred), quiet = TRUE))
}
for (g in c("EN", "PL", "FA")) {
  d <- cues %>% filter(group == g) %>% select(-group)
  all_cues <- fit_rf(d, voicing ~ ., mtry = 3)
  vot_only <- fit_rf(d, voicing ~ VOT_ms, mtry = 1)
  cat("\n", g, ": accuracy all cues =", round(all_cues$accuracy, 3),
      "| VOT only =", round(vot_only$accuracy, 3), "\n")
  print(roc.test(vot_only$roc, all_cues$roc))
  # variable importance with conditional permutation tests (book ch. 8.7.1.3).
  # The book uses varImp::varImpAUC(model, conditional = TRUE) (install.packages("varImp"));
  # party::varimp below is the accuracy-based version and needs no extra package.
  set.seed(42)
  vi <- varimp(all_cues$model, conditional = TRUE)
  print(sort(vi, decreasing = TRUE))
}

# ---- 6. wav2vec2 layers: PCA (10 dimensions) + Random Forest per layer ---------------
w2v <- read_csv("w2v2_layers.csv") %>%
  mutate(word = tolower(word),
         voicing = factor(ifelse(word %in% c("bob", "big", "bags", "go"), "voiced", "voiceless")))
acc <- map_dfr(sort(unique(w2v$layer)), function(L) {
  d <- filter(w2v, layer == L)
  p <- PCA(select(d, starts_with("d")), scale.unit = TRUE, ncp = 10, graph = FALSE)
  pcs <- as.data.frame(p$ind$coord) %>% mutate(voicing = d$voicing)
  r <- fit_rf(pcs, voicing ~ ., mtry = 3)
  tibble(layer = L, accuracy = r$accuracy)
})
acc
ggplot(acc, aes(layer, accuracy)) + geom_line() + geom_point() +
  labs(x = "wav2vec2 layer", y = "Voicing classification accuracy (out-of-bag)")

# ---- 7. (Optional) OpenSMILE eGeMAPS features: Random Forest on all 88 features ------
ege <- read_csv("egemaps_tokens.csv") %>%
  left_join(select(dat, key, voicing, group), by = "key") %>%
  filter(!is.na(voicing))
names(ege) <- make.names(names(ege))          # makes the long feature names safe for R formulas
ege_rf <- fit_rf(select(ege, -key, -group), voicing ~ ., mtry = round(sqrt(88)))
ege_rf$accuracy                                # compare with the acoustic-cue and wav2vec2 accuracies
