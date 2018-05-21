#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:05:38 2018

@author: nt
"""

ngram <- function(phrases, corpus='eng_2012', year_start = 1500,
                  year_end = 2008, smoothing = 3, count=FALSE,
                  tag = NULL, case_ins=FALSE) {
  stopifnot(is.character(phrases))
  if (length(phrases) > 12){
    phrases <- phrases[1:12]
    warning("Maximum number of phrases exceeded: only using first 12.")
  } }
  dfs <- lapply(corpus, function(corp) ngram_single(phrases, corpus=corp,
                                                    year_start=year_start,
                                                    year_end=year_end,
                                                    smoothing=smoothing,
                                                    tag=tag, case_ins))
  result <- do.call("rbind", dfs)
  result$Corpus <- as.factor(result$Corpus)
  class(result) <- c("ngram", class(result))
  attr(result, "smoothing") <- smoothing
  attr(result, "case_sensitive") <- TRUE
  if (count) result <- add_count(result)
  return(result)
}

ngram_single <- function(phrases, corpus, tag, case_ins, ...){
  phrases <- phrases[1:ifelse(length(phrases) < 13, length(phrases), 12)]
  if (!is.null(tag)) {
    if (grepl("NOUN|VERB|ADJ|ADV|PRON|DET|ADP|NUM|CONJ|PRT", tag))
      phrases = paste0(phrases, "_", gsub("_", "", tag))      
    else if (grepl("ROOT|START|END", tag))
      phrases = paste(paste0("_", tag, "_"), phrases)      
  }
  corpus_n <- get_corpus(corpus)
  if (is.na(corpus_n)) {
    warning("Invalid corpus name. Defaulting to 'eng_2012'", call.=FALSE)
    corpus_n <- get_corpus("eng_2012")
  }
  result <- data.frame()
  for (phrase in phrases) {
    df <- ngram_fetch(phrase, corpus_n, case_ins,...)
    if (NROW(df) > 0) {
      df$Corpus <- corpus
      result <- rbind(result, df)
    }
  }
  return(result)
}

ngram_fetch <- function(phrases, corpus, year_start,  year_end, smoothing, case_ins=FALSE) {
  query <- as.list(environment())
  if (case_ins) query["case_insensitive"] <- "on"
  query$phrases <- NULL
  query$case_ins <- NULL
  phrases <- phrases[phrases != ""]
  if (length(phrases)==0) stop("No valid phrases provided.")
  ng_url <- ngram_url(phrases, query)
#   print(ng_url)
  cert <- system.file("CurlSSL/cacert.pem", package = "RCurl")
  html <- strsplit(content(GET(ng_url, config(cainfo = cert)), "text"), "\n", perl=TRUE)[[1]]
  if (html[1] == "Please try again later.") stop('Server busy, answered "Please try again later."')
  result <- ngram_parse(html)
#   browser()
  if (NROW(result) > 0) result <- reshape2::melt(result, id.vars="Year", 
                                                 variable.name="Phrase",
                                                 value.name="Frequency")
  return(result)
}

ngram_url <- function(phrases, query=character()){
  url <- 'https://books.google.com/ngrams/graph'
#   url <- 'https://books.google.com/ngrams/interactive_chart'
  n <- length(phrases)
  for (i in 1:n){
    if (grepl("\\+|/", phrases[i])) phrases[i] <- paste0("(", phrases[i], ")")
    p <- phrases[i]
    if (!(Encoding(p) %in% c("unknown", "UTF-8"))){
      phrases[i] <- iconv(p, Encoding(p), "UTF-8")
    }   
  }
  phrases <- paste(curlEscape(str_trim(phrases)), collapse='%2c')
  if (phrases=="") stop("No valid phrases provided.")
  url <- paste0(url, "?content=", phrases) 
  if (length(query) > 0) url <- modify_url(url, query=query)
  url <- gsub("%28", "(", url)
  url <- gsub("%29", ")", url)
  url <- gsub("%20", "+", url)
  return(url)
}

ngram_parse <- function(html){
#   if (any(grepl("No valid ngrams to plot!<br>", html))) stop("No valid ngrams.") 
   if (any(grepl("No valid ngrams to plot!<br>", html))) return(data.frame())
  
  # Warn about character substitution
  lapply(grep("^Google has substituted ",
              gsub("<.?b.?>","", sub("Replaced (.*) to match how we processed the books",
                                              "Google has substituted \\1", html)),
              value=TRUE), warning, call. = FALSE)  
  data_line <- grep("var data", html)
  year_line <- grep("drawD3Chart", html)
  ngram_data <- fromJSON(sub(".*=", "", html[data_line]))
  years <- as.integer(strsplit(html[year_line], ",")[[1]][2:3])
  cols <- unlist(lapply(ngram_data, function(x) x$ngram))
  data <- as.data.frame(lapply(ngram_data[lapply(ngram_data, length) > 0],
                               function(x) x$timeseries))
  years <- seq.int(years[1], years[2])
  if (NROW(data)==0) return(data.frame())
  data <- cbind(years, data)
  colnames(data) <- c("Year", cols)
  data <- data[!grepl("\\*|\\(All\\)", names(data))]
  return(data)
}

get_corpus <- function(corpus){
  corpora <- c('eng_us_2012'=17, 'eng_us_2009'=5, 'eng_gb_2012'=18, 'eng_gb_2009'=6, 
           'chi_sim_2012'=23, 'chi_sim_2009'=11,'eng_2012'=15, 'eng_2009'=0,
           'eng_fiction_2012'=16, 'eng_fiction_2009'=4, 'eng_1m_2009'=1, 'fre_2012'=19, 'fre_2009'=7, 
           'ger_2012'=20, 'ger_2009'=8, 'heb_2012'=24, 'heb_2009'=9, 
           'spa_2012'=21, 'spa_2009'=10, 'rus_2012'=25, 'rus_2009'=12, 'ita_2012'=22)
  return(unname(corpora[corpus]))
}	
