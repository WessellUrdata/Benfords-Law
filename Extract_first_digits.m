clc;
close all;
clear;
workspace;
fontSize = 10;

filename = ['C:\Users\pedro\OneDrive\Ambiente de Trabalho\DISSERTAÇÃO\Dataset\cinco.csv_features.csv'];
t = readtable(filename);
vnc = readcell(filename,'Range',[2 2]);
calcula_primeiro_digito=cellfun(@(v)v(1),""+vnc)-'0';
disp(calcula_primeiro_digito)


digitos = (1:9).';
benford= log10(1+(1./digitos));
[nlinhas,ncolunas] = size(calcula_primeiro_digito);
c = unique(calcula_primeiro_digito);
counts=histc(calcula_primeiro_digito',1:max(calcula_primeiro_digito(:))).'
disp("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
 fprintf('Contagem dos primeiros digitos existentes em cada linha [figura]:\n');

%calcula a frequencia relativa de cada linha
disp(counts);
freq_Imagem = (counts ./ ncolunas).';
disp(freq_Imagem)

disp("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
 fprintf('Contagem total dos primeiros digitos existentes no dataset\n');

%%%%%%%%%%%%% Begin: conta todos os digitos do dataset %%%%%%%%%%%%%%%%%%
        conta = histcounts(calcula_primeiro_digito,[digitos;inf]);
        disp(conta)
        frequencia_relativa = (conta ./ (nlinhas * ncolunas)).';
        [corre, pvalue1]= corr(frequencia_relativa,benford)
        disp(frequencia_relativa)
        figure(1)
        x = 1:9;
        plot(x,benford,'r',x,frequencia_relativa,'b')
        title("Benford law")
        xlabel('Digits')
        ylabel('Relative frequencies')
        
disp("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

fprintf('Resultados das várias correlações\n')
disp("Pearson's Correlation:")
[corre1,pval] = corr(freq_Imagem,benford)

% Coeficiente de Spearman:
disp("Spearman's Correlation:")
[corre2,pval2] = corr(freq_Imagem,benford,"type","Spearman")

Correlacao = table(corre1,corre2);
P_Values = table(pval,pval2);
Novos_nomes_probabilidade = renamevars(Correlacao,["corre1","corre2"],["Pearson","Spearman"]);
Novos_nomes_p_value = renamevars(P_Values,["pval","pval2"],["P_Pearson","P_Spearman"]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PEARSON %%%%%%%%%%%%%%%%%%%%%%%% 
fP=fopen('Pearson.txt','w');
fprintf(fP,"Analysis based on Pearson's correlation\n");
fprintf(fP,"Test hypotheses:\n");
fprintf(fP,'H(0): Pearsons correlation coefficient is equal to zero, that is, there is no linear relationship between the two probabilities under study.\n');
fprintf(fP,'H(a): Pearsons correlation coefficient is different from zero, that is, there is a relationship between the two probabilities.\n');
fprintf(fP,'Rule that allows the decision:\n');
fprintf(fP,'The correlation coefficient measures the degree of association between the variables under study.\n');
fprintf(fP,'Do not reject H(0) if the degree of significance > alfa = 0,05\n');
fprintf(fP,'Reject H(0) and accept H(a) if the degree of significance <= alfa = 0,05\n\n');
fprintf(fP,"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n");


fprintf(fP,'Results:\n');
 for s=1:nlinhas
   for q=1:1 
     if(pval(s,q) < 0.001 && (all(corre1(s,q) > 0.1) && all(corre1(s,q) < 0.4)))
         fprintf(fP,'Imagem[%d]: Possible true picture, with weak correlation between the probabilities\n',s);
     elseif(pval(s,q) < 0.001 && (all(corre1(s,q) > 0.4) && all(corre1(s,q) < 0.7)))
         fprintf(fP,'Imagem[%d]: Possible true picture, with moderate correlation between the probabilities\n',s);
     elseif(pval(s,q) < 0.001 && (all(corre1(s,q) > 0.7) && all(corre1(s,q) < 0.9)))
         fprintf(fP,'Imagem[%d]: Possible true picture, with strong correlation between the probabilities\n',s);
     else
         fprintf(fP,'Imagem[%d]: Possible fake image\n',s);
     end
    end
 end
fprintf(fP,'\n\n');
fclose(fP);


% Results for comparison with labels:
fpl = fopen("Pearson_labels.txt","w");
 for l=1:nlinhas
   for y=1:1 
     if(pval(l,y) < 0.001)
         % && (all(corre1(l,y) > 0.1) && all(corre1(l,y) < 0.4)))
         fprintf(fpl,'%d,1.0\n',l);
%      elseif(pval(l,y) < 0.05)% && (all(corre1(l,y) > 0.4) && all(corre1(l,y) < 0.7)))
%          fprintf(fpl,'%d,1.0\n',l);
%      elseif(pval(l,y) < 0.05 && (all(corre1(l,y) > 0.7) && all(corre1(l,y) < 0.9)))
%          fprintf(fpl,'%d,1.0\n',l);
     else
         fprintf(fpl,'%d,0.0\n',l);
     end
    end
 end
fclose(fpl);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% SPEARMAN %%%%%%%%%%%%%%%%%%%%%%
fS=fopen('Spearman.txt','w');
fprintf(fS,"Analysis based on Spearman's correlation\n");
fprintf(fS,'The Spearman correlation coefficient does not require the variables to be linear\n');
fprintf(fS,"Test hypotheses:\n");
fprintf(fS,'H(0): Spearmans correlation coefficient is equal to zero, that is, there is no linear relationship between Benfords law and image features\n');
fprintf(fS,'H(a): Spearmans correlation coefficient is different from zero, that is, there is a relationship between Benfords law and image features.\n');

fprintf(fS,'Rule that allows the decision:\n');
fprintf(fS,'Decisive factor: if there is no relationship between the frequencies, the probability of the image being manipulated is very high.\n');
fprintf(fS,'Do not reject H(0) if the degree of significance > alpha = 0.001\n');
fprintf(fS,'Reject H(0) and accept H(a) if the degree of significance <= alpha = 0.001\n');
fprintf(fS,"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n");

fprintf(fS,'Results:\n');
 for s=1:nlinhas
   for q=1:1 
     if(pval2(s,q) < 0.001 && (all(corre2(s,q) >= 0) && all(corre2(s,q) < 0.8)))
         fprintf(fS,'Image[%d]: possible true image, with weak association\n',s);
     elseif(pval2(s,q) < 0.001 && (all(corre2(s,q) >= 0.5) && all(corre2(s,q) <= 1)))
         fprintf(fS,'Image[%d]: possible true image, with strong association\n',s);
     else
         fprintf(fS,'Image[%d]: possible fake image\n',s);
     end
    end
 end
fprintf(fS,'\n\n');
fclose(fS);

% Labels Spearman:

fSl = fopen("Spearman_labels.txt","w");
 for d=1:nlinhas
   for r=1:1 
     if(pval2(d,r) < 0.001)% && (all(corre2(d,r) >= 0) && all(corre2(d,r) < 0.8)))
         fprintf(fSl,'%d,1.0\n',d);
%      elseif(pval2(d,r) < 0.01 && (all(corre2(d,r) >= 0.5) && all(corre2(d,r) <= 1)))
%          fprintf(fSl,'%d,1.0\n',d);
     else
         fprintf(fSl,'%d,0.0\n',d);
     end
    end
 end
fprintf(fSl,'\n\n');
fclose(fSl);

% Two-simple Cramer-Von Misses distribution and criterion:

Real_values = cumsum(freq_Imagem)./sum(freq_Imagem);
Empirical_values = cumsum(benford)./sum(benford);
 N1 = length(Real_values(1:9,:));
 N2 = length(Empirical_values(1:9,1)); 
 N = N1+N2;
  CVM = trapz(((Empirical_values - Real_values).^2).',2); 
  Media = (1./6)+(1./(6.*N));
  Variancia = (1./45).*((N+1)./(N.^2)).*((4.*N1.*N2.*N-3.*(N1.^2+N2.^2)-2.*N1.*N2)./(4.*N1.*N2));
  Calculo_pval = abs(((CVM-Media)./(sqrt(45.*Variancia)))+(1./6));
  fprintf("cvm\n");
  disp(CVM)
  disp(Calculo_pval)


fcvm=fopen('Cramer-Von Mises.txt','w');
fprintf(fcvm,"Analysis based on Cramer-Von Mises correlation\n");
fprintf(fcvm,"Test hypotheses:\n");
fprintf(fcvm,'H(0): Cramer-Von Mises correlation coefficient is equal to zero, that is, there is no linear relationship between Benfords law and image features\n');
fprintf(fcvm,'H(a): Cramer-Von Mises correlation coefficient is different from zero, that is, there is a relationship between Benfords law and image features.\n');

fprintf(fcvm,'Rule that allows the decision:\n');
fprintf(fcvm,'Decisive factor: if there is no relationship between the frequencies, the probability of the image being manipulated is very high.\n');
fprintf(fcvm,'Do not reject H(0) if the degree of significance > alpha = 0.001\n');
fprintf(fcvm,'Reject H(0) and accept H(a) if the degree of significance <= alpha = 0.001\n');
fprintf(fcvm,"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n");

fCVM = fopen("cvm_labels.txt","w");
 for d=1:nlinhas
   for r=1:1 
     if(Calculo_pval(d,r) < 0.001)
         fprintf(fCVM,'%d,1.0\n',d);
     else
         fprintf(fCVM,'%d,0.0\n',d);
     end
    end
 end
fprintf(fCVM,'\n\n');
fclose(fCVM);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% GRAPHS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if nlinhas > 1 & nlinhas <=24 

figure(2)
n = freq_Imagem(1:9,1:24); %1:24
b = benford(1:9,1:1);
i = 1:2; %24
newYlabels = ["Figura"+i,"Benford"];
s = stackedplot([n,b],"DisplayLabels",newYlabels);
s.LineWidth = 1.5;
s.XLabel = "Digitos";
s.Title = "Lei de Benford - 1º digito";

elseif nlinhas > 24 & nlinhas <=100
box = nlinhas/floor(5)


% %%%%%%%%%%%%%%%%%%%%%%%%%%%%% entre 101 e 999 imagens &&&&&&&&&&&&&&&&&&&&
elseif nlinhas >101 & nlinhas <= 999 

imagens_por_figura = 15;
box2 = ceil(nlinhas/15); 
for k = 1:box2
figure(k) 
ind1 = 1+(k-1)*imagens_por_figura;
ind2 = min(nlinhas,ind1+imagens_por_figura-1);
n = freq_Imagem(1:9,ind1:ind2);
b = benford(1:9,1:1);
i = ind1:ind2;
newYlabels = ["Figure"+i,"Benford"];
s = stackedplot([n,b],"DisplayLabels",newYlabels);
s.LineWidth = 1.5;
s.XLabel = "Digits";
s.Title = "Benford law- 1º digit";
end
% 
elseif nlinhas >1000 & nlinhas <= 9999
imagens_por_figura = 15;
box2 = ceil(nlinhas/15); 
for k = 1:box2
figure(k) 
ind1 = 1+(k-1)*imagens_por_figura;
ind2 = min(nlinhas,ind1+imagens_por_figura-1);
n = freq_Imagem(1:9,ind1:ind2);
b = benford(1:9,1:1);
i = ind1:ind2;
newYlabels = ["Figure"+i,"Benford"];
s = stackedplot([n,b],"DisplayLabels",newYlabels);
s.LineWidth = 1.5;
s.XLabel = "Digits";
s.Title = "Benford law- 1º digit";
end
% 
% 
elseif nlinhas >10000 & nlinhas <= 99999 
imagens_por_figura = 15;
box2 = ceil(nlinhas/15); 
for k = 1:box2
figure(k) 
ind1 = 1+(k-1)*imagens_por_figura;
ind2 = min(nlinhas,ind1+imagens_por_figura-1);
n = freq_Imagem(1:9,ind1:ind2);
b = benford(1:9,1:1);
i = ind1:ind2;
newYlabels = ["Figure"+i,"Benford"];
s = stackedplot([n,b],"DisplayLabels",newYlabels);
s.LineWidth = 1.5;
s.XLabel = "Digits";
s.Title = "Benford law- 1º digit";
end
% 
% 
elseif nlinhas >1000000  & nlinhas <= 999999 

imagens_por_figura = 15;
box2 = ceil(nlinhas/15); 
for k = 1:box2
figure(k) 
ind1 = 1+(k-1)*imagens_por_figura;
ind2 = min(nlinhas,ind1+imagens_por_figura-1);
n = freq_Imagem(1:9,ind1:ind2);
b = benford(1:9,1:1);
i = ind1:ind2;
newYlabels = ["Figure"+i,"Benford"];
s = stackedplot([n,b],"DisplayLabels",newYlabels);
s.LineWidth = 1.5;
s.XLabel = "Digitos";
s.Title = "Lei de Benford - 1º digito";
end

end

figure(2)
scatter(corre1,corre2);
