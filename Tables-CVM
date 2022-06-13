clc;
close all;
clear;
workspace;
fontSize = 10;


filename = 'C:\Users\pedro\OneDrive\Ambiente de Trabalho\DISSERTAÇÃO\Dataset\cinco.csv_labels.csv';
Original_labels_from_images = readtable(filename);
Original_labels_from_images(1,:) = [];
S = load("cvm_labels.txt");
opts = detectImportOptions('cvm_labels.txt');
tabela = readtable('cvm_labels.txt',opts);
Apagar_primeira_coluna = removevars(tabela,"Var1");
New_names_from_original_labels = renamevars(Original_labels_from_images,["Var1","Var2"],["Image","OStatus"]);
New_names_from_Pearson_labels = renamevars(Apagar_primeira_coluna,"Var2","PStatus");
FinalDatasetToCompare = [New_names_from_original_labels New_names_from_Pearson_labels];

Array = table2array(FinalDatasetToCompare);
[Nlinhas,Ncolunas] = size(Array);

[Array23,ia,ix] = unique(Array(:,[2 3]),"rows");
s = accumarray(ix,1);
Res = [Array23,s];
fre = (s/280)*100;

fprintf("Legenda:\n");
fprintf("0  0 TN - True Positive\n"); % Relação: 0 0 - imagem falsa que acusa falsa
fprintf("0  1 FP - False Positive\n"); % Relação: 0 1 - imagem falsa que acusa verdadeira
fprintf("1  0 FN - False Negative\n"); % Relação: 1 1 - imagem verdadeira que acusa falsa
fprintf("1  1 TP - True Negative\n"); % Relação: 1 1 - imagem verdadeira que acusa verdadeira

fprintf(" Numero de ocorrências para 100 imagens verdadeiras e 100 falsas\n");
fprintf(" --------------------------\n");
fprintf("| 0   0  = %d --- %.2f%%   |\n",Res(1,3),fre(1,1));
fprintf("| 0   1  = %d --- %.2f%%    |\n",Res(2,3),fre(2,1));
fprintf(" --------------------------\n");
fprintf("| 1   0  = %d --- %.2f%%   |\n",Res(3,3),fre(3,1));
fprintf("| 1   1  = %d --- %.2f%%    |\n",Res(4,3),fre(4,1));
fprintf(" --------------------------\n");


% Acurracy

 P = Res(1,3) / (Res(1,3) + Res(2,3))

% Recall
R = Res(1,3) / (Res(1,3) + Res(3,3))

% f1 score
F1 = 2* ((P*R)/(P+R))

% ACC

A = (Res(1,3)+Res(4,3))/(Res(1,3)+Res(2,3)+Res(3,3)+Res(4,3))
