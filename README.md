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
<li>
  Common data enhancement methods include histogram-based approaches, filtering techniques, and second-order Laplacian operators. Among these, Adaptive Histogram Equalization (AHE) improves the dynamic range of CT response values by transforming the original data histogram into a uniform distribution, effectively enhancing image contrast (Jam et al., 2021). However, due to the subtle differences between weak fractures and the surrounding matrix in CT response values, traditional AHE often induces a "mosaic effect", characterized by block-like artifacts arising from localized over-enhancement. Contrast Limited Adaptive Histogram Equalization (CLAHE) mitigates this issue by restricting the extent of local contrast amplification, thereby reducing mosaic artifacts. Nonetheless, CLAHE still exhibits limited capability to enhance weak edges and subtle details within low-contrast regions.
To address these limitations, the present study proposes a novel adaptive histogram equalization method combined with a sharpening convolution kernel. The implementation procedure is as follows:
  
</li>












