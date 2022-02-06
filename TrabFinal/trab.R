getwd()

library(arules)
library(pander)
library(data.table)
library(stringr)
# library(dplyr)
# library(fpp2)
# library(arulesviz)

col_names <- read.table('TopAcoes.txt', sep = "\t", header = FALSE)

data <- read.csv('2020closePrice SAX-240_60_10.csv', header = FALSE, skip = 1)
data_column <- data[2]
data <- data[3:46]

# renomeia as colunas com os nomes apropriados
colnames(data) <- col_names

# separa os precos das acoes
data[data <= 'e'] <- 'abaixo'
data[data > 'e'] <- 'acima'

# add coluna da data
data <- cbind(data_column, data)
# renomeia a coluna recem adicionada
names(data)[names(data) == 'V2'] <- 'Data'

# discretiza os valores
for (i in 1:45){data[,i] <- as.factor(data[,i])}

# rules <- apriori(data, parameter = list(minlen=2, sup=0.75, conf=0.8))

# associacoes petrobras
rules <- apriori(data, parameter = list(minlen=2, conf=0.7), appearance = list(lhs = c("PETR4.SA=acima"), default = "rhs"))

inspect(sort(rules, by="confidence"))

# save current dataframe to csv
write.csv(data,"cleaned.csv", row.names = FALSE)


# itemFrequencyPlot(base, topN = 10, main = "\nTop 10 itens mais frequentes\n", type = 'absolute')