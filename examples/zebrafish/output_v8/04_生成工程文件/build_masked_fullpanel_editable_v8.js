
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.defineLayout({ name:'CUSTOM', width:14.48, height:10.86 });
pptx.layout = 'CUSTOM';
pptx.author = 'Yuzhoujun Fig2Edit';
pptx.subject = 'Masked full-panel editable reconstruction';
const assets = {"panel_A": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/complete_panels_2x/panel_A_complete_2x.png", "panel_A_masked": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/masked_full_panels_2x/panel_A_masked_full_2x.png", "panel_B": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/complete_panels_2x/panel_B_complete_2x.png", "panel_B_masked": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/masked_full_panels_2x/panel_B_masked_full_2x.png", "panel_C": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/complete_panels_2x/panel_C_complete_2x.png", "panel_C_masked": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/masked_full_panels_2x/panel_C_masked_full_2x.png", "panel_D": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/complete_panels_2x/panel_D_complete_2x.png", "panel_D_masked": "/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/03_高清无损素材/masked_full_panels_2x/panel_D_masked_full_2x.png"};
function img(slide,key,x,y,w,h) { slide.addImage({path:assets[key],x,y,w,h}); }
function text(slide,s,x,y,w,h,opt={}) { slide.addText(s,Object.assign({x,y,w,h,fontFace:'Arial',fontSize:10,color:'000000',margin:0.01,fit:'shrink',breakLine:false},opt)); }
function line(slide,x1,y1,x2,y2,opt={}) { slide.addShape(pptx.ShapeType.line,Object.assign({x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color:'000000',width:1.1}},opt)); }
function arrow(slide,x1,y1,x2,y2,opt={}) { slide.addShape(pptx.ShapeType.line,Object.assign({x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color:'000000',width:1.2,endArrowType:'triangle'}},opt)); }
function rect(slide,x,y,w,h,c,opt={}) { slide.addShape(pptx.ShapeType.rect,Object.assign({x,y,w,h,fill:{color:c},line:{color:c,width:0.2}},opt)); }
function t(slide,s,x,y,w,h,opt={}) { text(slide,s,x/100,y/100,w/100,h/100,opt); }
function l(slide,x1,y1,x2,y2,opt={}) { line(slide,x1/100,y1/100,x2/100,y2/100,opt); }
function a(slide,x1,y1,x2,y2,opt={}) { arrow(slide,x1/100,y1/100,x2/100,y2/100,opt); }
function r(slide,x,y,w,h,c,opt={}) { rect(slide,x/100,y/100,w/100,h/100,c,opt); }
function addPanels(slide, masked=false) {
  slide.background = { color:'FFFFFF' };
  img(slide, masked ? 'panel_A_masked' : 'panel_A',0.04,0.04,6.92,4.82);
  img(slide, masked ? 'panel_B_masked' : 'panel_B',7.04,0.04,7.40,4.82);
  img(slide, masked ? 'panel_C_masked' : 'panel_C',0.04,4.92,6.26,4.64);
  img(slide, masked ? 'panel_D_masked' : 'panel_D',6.38,4.92,8.06,4.64);
}
function caption(slide) {
  t(slide,'Top:',30,992,38,18,{fontSize:11,bold:true});
  t(slide,'Cross-sectional schematic and hierarchical clustering heatmap reveal gene expression clusters corresponding to different tissues along the dorsal–ventral axis of the zebrafish tail.',68,992,1285,18,{fontSize:10.5});
  t(slide,'Bottom:',30,1022,62,18,{fontSize:11,bold:true});
  t(slide,'Representative image shows Tg(kdrl:GFP)+ endothelial cells outlining the CHT. Schematic shows the strategy for isolating endothelial cells from kdrl:GFP',92,1022,1205,18,{fontSize:10.5});
  t(slide,'transgenic embryos by FACS for RNA-seq.',30,1048,405,18,{fontSize:10.5});
}
function labels(slide) {
  t(slide,'A',16,16,36,32,{fontSize:24,bold:true}); t(slide,'B',720,16,36,32,{fontSize:24,bold:true});
  t(slide,'C',16,505,36,32,{fontSize:24,bold:true}); t(slide,'D',650,505,36,32,{fontSize:24,bold:true});
  t(slide,'Cross-section of zebrafish tail at 72 hpf',142,16,430,24,{fontSize:13,bold:true,align:'center'});
  t(slide,'Dorsal–ventral axis',238,42,230,22,{fontSize:12,italic:true,align:'center'});
  t(slide,'Hierarchical clustering of tissue-specific gene expression',805,16,530,24,{fontSize:13,bold:true,align:'center'});
  t(slide,'72 hpf zebrafish tail (dorsal–ventral axis)',902,43,392,18,{fontSize:10.5,italic:true,align:'center'});
  t(slide,'Tg(kdrl:GFP)+ endothelial cells (ECs) define the CHT',108,504,475,26,{fontSize:13,bold:true,italic:true,align:'center'});
  t(slide,'Experimental strategy to isolate endothelial cells from kdrl:GFP',785,516,520,25,{fontSize:12.3,bold:true,align:'center'});
  t(slide,'embryos for RNA-seq (FACS workflow)',890,544,350,25,{fontSize:12.3,bold:true,align:'center'});
  t(slide,'Dorsal',28,92,70,20,{fontSize:10,bold:true}); t(slide,'Ventral',20,352,80,22,{fontSize:10,bold:true});
  a(slide,48,120,48,348); a(slide,48,348,48,120);
  [[360,143,510,143],[425,193,512,193],[322,235,510,235],[455,280,510,280],[334,326,497,326]].forEach(v=>l(slide,...v));
  [['Spinal cord',518,136,'7040AA'],['Muscle',518,186,'D8262F'],['Notochord',518,228,'275FD3'],['Epidermis',518,273,'B17435']].forEach(v=>t(slide,v[0],v[1],v[2],112,22,{fontSize:11,color:v[3]}));
  t(slide,'Caudal hematopoietic',504,318,170,22,{fontSize:11,bold:true,color:'0B7F2A'});
  t(slide,'tissue (CHT)',504,342,112,20,{fontSize:11,bold:true,color:'0B7F2A'});
  t(slide,'HSPCs reside in the CHT',504,367,175,20,{fontSize:10});
  const groups=[['Spinal cord','(n=142 genes)',805,'7040AA'],['Muscle','(n=186 genes)',930,'D8262F'],['Notochord','(n=88 genes)',1045,'275FD3'],['Epidermis','(n=124 genes)',1160,'B17435'],['CHT','(n=156 genes)',1280,'0B7F2A']];
  groups.forEach(g=>{r(slide,g[2]-50,113,110,10,g[3]); t(slide,g[0],g[2]-48,127,96,16,{fontSize:8.4,bold:true,color:g[3],align:'center'}); t(slide,g[1],g[2]-48,144,96,14,{fontSize:7.4,italic:true,align:'center'});});
  const clusters=[['Cluster 1','Spinal cord','enriched',1350,172,'7040AA'],['Cluster 2','Muscle','enriched',1350,228,'D8262F'],['Cluster 3','Notochord','enriched',1350,284,'275FD3'],['Cluster 4','Epidermis','enriched',1350,340,'B17435'],['Cluster 5','CHT enriched','(hematopoietic)',1350,396,'0B7F2A']];
  clusters.forEach(c=>{r(slide,c[3]-18,c[4]-8,4,45,c[5]); t(slide,c[0],c[3],c[4]-4,78,13,{fontSize:7.3,bold:true,color:c[5]}); t(slide,c[1],c[3],c[4]+12,84,13,{fontSize:7.1}); t(slide,c[2],c[3],c[4]+27,86,13,{fontSize:7.1});});
  t(slide,'Expression (z-score)',970,408,130,15,{fontSize:8.5,bold:true,align:'center'});
  r(slide,950,426,85,14,'003A9B'); r(slide,1035,426,42,14,'222222'); r(slide,1077,426,43,14,'F1D200');
  t(slide,'-2',950,446,16,12,{fontSize:7.5,align:'center'}); t(slide,'0',1030,446,16,12,{fontSize:7.5,align:'center'}); t(slide,'2',1112,446,16,12,{fontSize:7.5,align:'center'});
  t(slide,'Low',940,464,36,14,{fontSize:8.5,color:'275FD3',align:'center'}); t(slide,'High',1103,464,40,14,{fontSize:8.5,color:'E2B100',align:'center'});
  t(slide,'Tg(kdrl:GFP)+ ECs',24,535,182,20,{fontSize:11,bold:true,italic:true,color:'00CC36'});
  t(slide,'Spinal cord',36,604,90,18,{fontSize:10,color:'FFFFFF'}); t(slide,'Muscle',46,673,65,18,{fontSize:10,color:'FFFFFF'}); t(slide,'Notochord',39,729,88,18,{fontSize:10,color:'FFFFFF'});
  l(slide,115,614,145,614,{line:{color:'FFFFFF',width:1}}); l(slide,100,684,145,684,{line:{color:'FFFFFF',width:1}}); l(slide,105,740,145,740,{line:{color:'FFFFFF',width:1}});
  t(slide,'GFP (kdrl)',515,535,90,18,{fontSize:10,bold:true,italic:true,color:'00CC36'});
  t(slide,'DAPI (nuclei)',515,557,100,18,{fontSize:10,color:'3262FF'}); t(slide,'α-Tubulin',515,579,92,18,{fontSize:10,bold:true,color:'FF2BD1'});
  l(slide,395,795,452,795,{line:{color:'FFFFFF',width:1}});
  t(slide,'Caudal hematopoietic',454,786,158,18,{fontSize:8.6,bold:true,color:'00CC36'});
  t(slide,'tissue (CHT)',454,805,96,18,{fontSize:8.6,bold:true,color:'00CC36'});
  t(slide,'Outlined by Tg(kdrl:GFP)+',424,835,135,18,{fontSize:7.7,color:'FFFFFF',italic:true});
  t(slide,'endothelial cells',424,854,120,18,{fontSize:7.7,color:'FFFFFF'});
  t(slide,'Dorsal',28,843,55,14,{fontSize:8.4,color:'FFFFFF'}); t(slide,'Ventral',28,912,60,14,{fontSize:8.4,color:'FFFFFF'});
  a(slide,46,865,46,900,{line:{color:'FFFFFF',width:1,endArrowType:'triangle'}}); a(slide,46,900,46,865,{line:{color:'FFFFFF',width:1,endArrowType:'triangle'}});
  t(slide,'50 μm',558,900,48,14,{fontSize:8.4,color:'FFFFFF'});
  [['1. kdrl:GFP',730,616,1],['embryo (72 hpf)',720,638,0],['2. Whole-embryo',935,616,1],['dissociation',950,638,0],['3. FACS isolation of',1108,616,1],['GFP+ ECs',1142,638,0],['4. RNA-seq',1310,616,1],['analysis',1325,638,0],['Single-cell',910,850,0],['suspension',918,872,0],['GFP–',1092,895,0],['cells',1100,915,0],['GFP+ ECs',1166,895,0],['(collected)',1170,915,0],['Transcriptome profiling',1286,895,0],['of endothelial cells',1304,918,0]].forEach(v=>t(slide,v[0],v[1]-45,v[2]-12,90,18,{fontSize:v[3]?9:8.2,bold:!!v[3],align:'center'}));
  a(slide,845,713,884,713); a(slide,995,713,1040,713); a(slide,1228,713,1270,713);
  t(slide,'GFP+ vasculature outlines',665,863,160,16,{fontSize:8.5,bold:true,color:'0A8A2A'});
  t(slide,'the CHT in the tail',690,886,110,16,{fontSize:8.5,bold:true,color:'0A8A2A'});
}
const s1 = pptx.addSlide();
addPanels(s1,false);
caption(s1);
s1.addNotes('Slide 1: original fidelity version with four complete high-resolution panel image layers.');
const s2 = pptx.addSlide();
addPanels(s2,true);
labels(s2);
caption(s2);
s2.addNotes('Slide 2: masked full-panel editable version. Panel images remain complete; text/arrow regions are locally masked and rebuilt as editable objects.');
pptx.writeFile({fileName:"/Users/cosmosyuzhoujun/Documents/skill研究/yuzhoujun-fig2edit/examples/zebrafish/output_v8/01_最终文件/zebrafish_masked_fullpanel_editable_v8.pptx"});
