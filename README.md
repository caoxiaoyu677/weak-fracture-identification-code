# weak-fracture-identification-code
Code for our paper on fracture detection in CT core samples.
## <li>A Novel Approach for Recognizing Weak Fractures in Hydraulic Fracturing of Rock Core</li>

## INTRODUCTION
<li><strong>Fracture identification and quantitative analysis in core-scale hydraulic fracturing experiments represent a critical technical approach for in-depth investigation of fracture initiation, propagation, and spatial distribution patterns during hydraulic fracturing. Hydraulic fractures typically exhibit low contrast, indistinct boundaries, and high discontinuity, rendering conventional fracture detection methods effective primarily for strong fractures but limited in identifying weaker fractures. To address these limitations associated with weak fractures, this study proposes a novel identification approach consisting of four principal stages: (1) data preprocessing, involving fracture enhancement and noise-reduction filtering; (2) precise fracture extraction using the ant-tracking algorithm; (3) fracture classification employing a clustering algorithm to effectively distinguish strong from weak fractures; and (4) reconstruction of the three-dimensional fracture model of rock cores by integrating both strong and weak fractures. To validate the performance and reliability of the proposed approach, fracture identification was conducted on two shale core samples from the Longmaxi Formation using multiple fracture recognition techniques. Comparative analysis indicates that the proposed approach significantly outperforms conventional thresholding and level-set methods by effectively enhancing the visibility of weak fracture information and accurately preserving fracture details. Thus, the proposed method demonstrates superior effectiveness and robustness for identifying weak fractures in rock core experiments.</strong></li>

### <li> FLOWCHART OF FRACTURE DETECTION AND CLASSIFICATION : </li>
<img align= center height=450px src=https://user-images.githubusercontent.com/75990647/192298994-d80bb374-568c-4906-a10b-75958a3f9c1f.png>
<li>The workflow of the proposed approach initiates with importing raw CT slice datasets (Figure 1a). Weak fractures typically exhibit CT response values closely resembling those of the surrounding rock matrix, complicating their accurate differentiation and reliable identification. To enhance fracture visibility, an adaptive histogram equalization technique combined with a sharpening convolution kernel is applied to the raw CT slices, generating fracture-enhanced data (Figure 1b). Although this step substantially improves fracture contrast, it concurrently amplifies noise of varying intensities and spatial distributions, adversely affecting subsequent analyses. To mitigate this issue, a hybrid noise-reduction strategy utilizing a combination of bilateral and Gabor filtering is employed, effectively preserving fracture details while reducing unwanted noise, thus producing clean and structurally detailed datasets (Figure 1c).
Subsequently, the ant-tracking algorithm is implemented, leveraging its heuristic searching capability to effectively identify continuous fracture pathways (Figure 1d). To enhance the precision of fracture representation, identified fracture paths undergo further refinement, yielding detailed fracture skeletons (Figure 1e). Finally, fractures are systematically classified into strong and weak categories based on their distinct CT response characteristics, resulting in accurate and comprehensive fracture identification datasets (Figure 1f).</li>

### ------------------------------------ METHODOLOGY ---------------------------------------- 
<ul><li><strong> FRCTURE EEHANCEMENT</strong></li></ul>
<ul><ul>
<li>
  Common data enhancement methods include histogram-based approaches, filtering techniques, and second-order Laplacian operators. Among these, Adaptive Histogram Equalization (AHE) improves the dynamic range of CT response values by transforming the original data histogram into a uniform distribution, effectively enhancing image contrast (Jam et al., 2021). However, due to the subtle differences between weak fractures and the surrounding matrix in CT response values, traditional AHE often induces a "mosaic effect", characterized by block-like artifacts arising from localized over-enhancement. Contrast Limited Adaptive Histogram Equalization (CLAHE) mitigates this issue by restricting the extent of local contrast amplification, thereby reducing mosaic artifacts. Nonetheless, CLAHE still exhibits limited capability to enhance weak edges and subtle details within low-contrast regions.
To address these limitations, the present study proposes a novel adaptive histogram equalization method combined with a sharpening convolution kernel. The implementation procedure is as follows:</li>
<li>
  To validate the effectiveness of the proposed enhancement method, three representative CT slices (Figure 2) were selected for comparative analysis. Slice I features one strong fracture and multiple complex weak fractures (Figure 2 Ia), Slice II has one strong fracture and three weak fractures (Figure 2 IIa), and Slice III comprises one strong fracture and two weak fractures (Figure 2 IIIa). The enhancement results (Figure 2 Ib, IIb, and IIIb) demonstrate substantial improvement in contrast between fractures and the surrounding matrix, significantly mitigating the blur and potential loss of weak fracture details commonly associated with noise amplification during traditional enhancement processes. Nevertheless, some noise amplification remains inevitable, manifesting with non-uniform intensity and spatial distributions, potentially affecting subsequent processing steps.
  <ul><img align= center height=450px src=https://user-images.githubusercontent.com/75990647/192298994-d80bb374-568c-4906-a10b-75958a3f9c1f.png></ul></li>
</ul></ul>
<ul><li><strong> FILTERING PROCESS</strong></li></ul>
<ul><ul>
<li>To mitigate the amplified noise introduced during fracture enhancement, a hybrid filtering strategy integrating bilateral filtering and Gabor filtering is implemented. Initially, bilateral filtering is employed for global noise suppression by constructing a dual-weight function that simultaneously considers spatial proximity and grayscale similarity, effectively smoothing noise while preserving fracture edge integrity. Subsequently, Gabor filtering is utilized to eliminate residual fine-scale noise and enhance local fracture structural and textural characteristics.</li></ul></ul>
<ul><li><strong>Ant Tracking Algorithm ANT TRACKING ALGORITHM</strong></li></ul>
<ul><ul>
<li>The ant tracking algorithm is a novel optimization method inspired by the collective foraging behavior of ants, where individuals release pheromones along traveled paths and preferentially move toward regions with higher pheromone intensity (Wu et al., 2014). Due to its robustness and adaptability, the algorithm has been widely applied in fields such as fault detection, image tracking, and path planning (Xie et al., 2022; S. Choi et al., 2024; Xia et al., 2024). When applied to core CT data analysis, the algorithm simulates ants' adaptive path-finding behaviors, enabling reliable identification of continuous fracture pathways, even under weak signal conditions.
In the ant colony algorithm, the optimal path selection is abstracted as a global path-planning problem comprising two fundamental processes: path construction and pheromone updating (Li et al., 2023). </li>
<li>
  When applied to fracture identification from core CT data, fractures typically manifest as regions with significant gradients in CT response values. Thus, virtual ants preferentially navigate toward areas exhibiting higher intensity gradients. During the iterative process, multiple ants traverse the CT scan dataset guided by local pheromone concentrations, continuously depositing pheromones along probable fracture pathways. Consequently, fracture regions experience pheromone accumulation, reinforcing path visibility. Conversely, non-fracture regions experience pheromone evaporation, ensuring clear differentiation of fracture structures from the surrounding rock matrix.
</li>
</ul></ul>
<ul><li><strong>Differentiation of Strong and Weak Fractures</strong></li></ul>
<ul><ul>
<li>
    The CT datasets obtained from hydraulically fractured cores can be represented as a sequence of two-dimensional CT slices (Figure 3a), each potentially containing multiple fractures characterized by varying rupture intensities. Typically, strong fractures possess larger apertures, yielding lower CT response values, and appear as prominent dark or black streaks. Conversely, weak fractures exhibit narrower apertures, higher CT values, and appear as thin, grey to light-grey streaks with indistinct edges (Figure 3b). Given the notable differences in CT response distributions between strong and weak fractures, a K-means clustering approach is utilized to effectively classify these fracture types.
    <ul><img align= center height=450px src=https://user-images.githubusercontent.com/75990647/192298994-d80bb374-568c-4906-a10b-75958a3f9c1f.png></ul></li>
<li>
    Initially, the original CT dataset is loaded (Figure 4a). Subsequently, the fracture skeleton is extracted following the proposed fracture identification workflow (Figure 4b). The CT response values corresponding to the two-dimensional coordinates of the identified fracture skeletons are then retrieved. These values are clustered into two distinct groups using the K-means clustering algorithm, and the mean CT response values for each cluster are calculated. Given that strong fractures generally present lower average CT response values due to their larger apertures, the cluster with the lower mean CT response is designated as representing strong fractures, whereas the cluster with the higher mean CT response corresponds to weak fractures. Consequently, strong fractures are visualized and marked in red according to their coordinates, clearly distinguishing them from weak fractures (Figure 4c). This clustering-based differentiation strategy enables accurate classification and detailed quantitative analysis of strong and weak fracture populations within hydraulically fractured cores, facilitating subsequent comprehensive fracture characterization and modeling.
    <ul><img align= center height=450px src=https://user-images.githubusercontent.com/75990647/192298994-d80bb374-568c-4906-a10b-75958a3f9c1f.png></ul></li>
</ul></ul>

### ------------------------------------ DEMO ---------------------------------------- 
### Examples : 
 <img src=https://user-images.githubusercontent.com/75990647/192364958-662bf141-95f8-4836-ad9e-dacbd4d97338.jpg
 width="400px"/>
<img src=https://user-images.githubusercontent.com/75990647/192365094-9080ea94-d34d-469c-bd29-df20d82ee657.jpg
 width="400px"/>
 
<img src=https://user-images.githubusercontent.com/75990647/192308302-3f836f7b-4d7b-4419-b5c0-8de27f1e4dc0.jpg width="400px"/>
<img src=https://user-images.githubusercontent.com/75990647/192308594-ffe78b53-8b29-4003-bcf6-b6dc4fb71512.jpg width="400px"/>







