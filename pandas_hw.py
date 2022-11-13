# First things first, we need to import all necessary modules which are listed in the requirements.txt. This is crucial!
# 1. We have 2 functions to read our data
## 1.1. This function takes a bed file, gives it appropriate headers and returns it in a nicely workable view.
def read_bed6(input_file):
    resbed = pd.read_csv(input_file, sep='\t', header=None)
    resbedheader = ['chrom', 'chromStart', 'chromEnd', 'name', 'score', 'strand']
    resbed.columns = resbedheader[:len(resbed.columns)]
    return resbed
## Example usage with our bed file  
bedfile = read_bed6('alignment.bed')

## 1.2. This function takes a gff file, gives it appropriate headers and returns it in a nicely workable view.
def read_gff(input_file):
    resgff = pd.read_csv(input_file, header=None, skiprows=1, sep = '\t')
    resgffheader = ['chrom', 'source', 'type', 'chromStart', 'chromEnd','score', 'strand', 'phase', 'attributes']
    resgff.columns = resgffheader[:len(resgff.columns)]
    return resgff
## Example usage with our gff file    
gfffile = read_gff("rrna_annotation.gff")

## 1.3. To use the information about rRNA type we extract it from the column and crop it for convenience
gfffile['attributes'] = gfffile['attributes'].str.split(';|=| ', expand = True)[3]
datasub = gfffile.groupby('chrom')['attributes'].value_counts().unstack()

## Then we plot the distribution of rRNA types per chromosome (reference fragments)
ax = datasub.plot(kind='bar', figsize=(7, 5), xlabel='Sequence', ylabel='Count', rot=0)
ax.legend(title='RNA type', bbox_to_anchor=(1, 1), loc='upper left')
plt.xticks(rotation=90);

## 1.4 To understand which reference fragments intersect with our data, we invent the alternative BEDtools intersect tool and extract only positions which do intersect
mrgd = gfffile.merge(bedfile, on = 'chrom')
mrgd[(mrgd['chromStart_x'] > mrgd['chromStart_y']) & (mrgd['chromEnd_x'] < mrgd['chromEnd_y'])]

# 2. To visualize some data of differential gene expression we read it from a .gz file.
diff_expr = pd.read_table('diffexpr_data.tsv.gz')

## 2.1 We will need to color our data based on some conditions, so we write them, our decision based on them and desirable colors to some variables.
conditions = [
    (diff_expr['logFC'] >= 0) & (diff_expr['log_pval'] >= 1.3),
    (diff_expr['logFC'] < 0) & (diff_expr['log_pval'] >= 1.3),
    (diff_expr['logFC'] >= 0) & (diff_expr['log_pval'] < 1.3),
    (diff_expr['logFC'] < 0) & (diff_expr['log_pval'] < 1.3)
    ]
values = ['Significantly upregulated', 'Significantly downregulated', 'Nonsignificantly upregulated', 'Nonsignificantly downregulated']
colors = {'Significantly upregulated':'orange', 'Significantly downregulated':'blue', 'Nonsignificantly upregulated':'red', 'Nonsignificatly downregulated':'green'}

## Then we write our decisions to our file
diff_expr['cat'] = np.select(conditions, values)

## We will also need some probably significant and probably unsignificant positions later
### Get 2 genes with maximum log_pval
max_log_p = diff_expr.query('log_pval > 1.3').iloc[0:2]
### Get 2 genes with minimum log_pval
min_log_p = diff_expr.query('log_pval > 1.3')[::-1].iloc[0:2]

## Finally, we can start plotting with Seaborn package
a4_dims = (11.7, 8.27)
fig, ax = plt.subplots(figsize=a4_dims)
sns.scatterplot(x="logFC", y="log_pval", data=diff_expr, s=15, 
                hue = 'cat', alpha = 1, palette = ['red','orange','green','blue'], 
                legend='full', linewidth=0)
plt.axvline(0, 10, 0, linestyle = '--', color = 'gray', label = 'cat')
plt.axhline(1.3, 10, 0, linestyle = '--', color = 'gray')
plt.title("Volcano plot", weight='bold', style = 'italic', size = 17)
plt.xlabel("log$_2$ (fold change)", weight='bold', style = 'italic')
plt.ylabel("-log$_{10}$ (p-value correction)", style = 'italic', weight='bold')
plt.text(7, 4, 'p value = 0.05', c='grey', size='small', weight='bold')
plt.annotate(max_log_p.iloc[0][0], (max_log_p.iloc[0][1], max_log_p.iloc[0][4]), weight='bold',
             xytext=(max_log_p.iloc[0][1], max_log_p.iloc[0][4] + 12), 
             arrowprops=dict(arrowstyle='->', color = 'red'))
plt.annotate(max_log_p.iloc[1][0], (max_log_p.iloc[1][1], max_log_p.iloc[1][4]), weight='bold',
             xytext=(max_log_p.iloc[1][1], max_log_p.iloc[1][4] + 12), 
             arrowprops=dict(arrowstyle='->', color = 'red'))
plt.annotate(min_log_p.iloc[0][0], (min_log_p.iloc[0][1], min_log_p.iloc[0][4]), weight='bold',
             xytext=(min_log_p.iloc[0][1], min_log_p.iloc[0][4] + 12), 
             arrowprops=dict(arrowstyle='->', color = 'red'))
plt.annotate(min_log_p.iloc[1][0], (min_log_p.iloc[1][1], min_log_p.iloc[1][4]), weight='bold',
             xytext=(min_log_p.iloc[1][1], min_log_p.iloc[1][4] + 12), 
             arrowprops=dict(arrowstyle='->', color = 'red'))
