import FWCore.ParameterSet.Config as cms

from DQM.SiPixelPhase1Common.HistogramManager_cfi import *

StandardSpecifications1D.append(
    Specification(PerLayer1D).groupBy("PXBarrel|PXForward/PXLayer|PXDisk/OnlineBlock") # per-layer with history for online
                             .groupBy("PXBarrel|PXForward/PXLayer|PXDisk", "EXTEND_Y")
                             .save()
                             .custom()
                             .save()
)
StandardSpecifications1D.append(
    Specification().groupBy("PXBarrel|PXForward/OnlineBlock") # per-layer with history for online
                   .groupBy("PXBarrel|PXForward", "EXTEND_Y")
                   .save()
                   .custom()
                   .save()
)

StandardSpecifications1D_Num.append(
    Specification(PerLayer1D).groupBy("PXBarrel|PXForward/PXLayer|PXDisk/OnlineBlock/DetId/Event") # per-layer with history for online
                             .reduce("COUNT")
                             .groupBy("PXBarrel|PXForward/PXLayer|PXDisk/OnlineBlock") 
                             .groupBy("PXBarrel|PXForward/PXLayer|PXDisk", "EXTEND_Y")
                             .save()
                             .custom()
                             .save()
)
StandardSpecifications1D_Num.append(
    Specification().groupBy("PXBarrel|PXForward/OnlineBlock/DetId/Event") # per-layer with history for online
                   .reduce("COUNT")
                   .groupBy("PXBarrel|PXForward/OnlineBlock") 
                   .groupBy("PXBarrel|PXForward", "EXTEND_Y")
                   .save()
                   .custom()
                   .save()
)

# Configure Phase1 DQM for Phase0 data
SiPixelPhase1Geometry.n_inner_ring_blades = 24 # no outer ring

# Turn on 'online' harvesting. This has to be set before other configs are 
# loaded (due to how the DefaultHisto PSet is later cloned), therefore it is
# here and not in the harvestng config.
DefaultHisto.perLumiHarvesting = True

# Pixel Digi Monitoring
from DQM.SiPixelPhase1Digis.SiPixelPhase1Digis_cfi import *
SiPixelPhase1DigisAnalyzer.src = cms.InputTag("siPixelDigis") # adapt for real data

# Cluster (track-independent) monitoring
from DQM.SiPixelPhase1Clusters.SiPixelPhase1Clusters_cfi import *

# We could overwrite the Harvesters like this, and use the custom() steps to
# perform resetting of histograms.
#SiPixelPhase1ClustersHarvester = cms.EDAnalyzer("SiPixelPhase1OnlineHarvester",
#    histograms = SiPixelPhase1ClustersConf,
#    geometry = SiPixelPhase1Geometry
#)


# Raw data errors
from DQM.SiPixelPhase1RawData.SiPixelPhase1RawData_cfi import *

PerModule.enabled = True

siPixelPhase1OnlineDQM_source = cms.Sequence(SiPixelPhase1DigisAnalyzer
                                            + SiPixelPhase1ClustersAnalyzer
                                            + SiPixelPhase1RawDataAnalyzer
                                            )

siPixelPhase1OnlineDQM_harvesting = cms.Sequence(SiPixelPhase1DigisHarvester 
                                                + SiPixelPhase1ClustersHarvester
                                                + SiPixelPhase1RawDataHarvester
                                                )
