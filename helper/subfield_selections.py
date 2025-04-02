campaign_subfields = """{
                        ...CampaignData
                        __typename
                      }
                    }
                    
                    fragment CampaignData on Campaign {
                      id
                      name
                      status {
                        id
                        name
                        __typename
                      }
                      marketTarget
                      targetGeo
                      agency {
                        ...AgencyBase
                        __typename
                      }
                      client {
                        id
                        name
                        naming
                        code
                        __typename
                      }
                      coBrands {
                        id
                        name
                        __typename
                      }
                      brand {
                        id
                        name
                        code
                        __typename
                      }
                      product {
                        id
                        name
                        code
                        brands {
                          id
                          name
                          __typename
                        }
                        __typename
                      }
                      department {
                        id
                        __typename
                      }
                      budget
                      startOn
                      finishOn
                      targetAudience
                      conditions
                      createdAt
                      updatedAt
                      status {
                        id
                        name
                        code
                        __typename
                      }
                      code
                      documents {
                        id
                        code
                        name
                        path
                        size
                        __typename
                      }
                      approvedMplan {
                        id
                        __typename
                      }
                      isReportReady
                      representative {
                        id
                        name
                        surname
                        middleName
                        __typename
                      }
                      canRepresentativeSetEmpty
                      __typename
                    }
                    
                    fragment AgencyBase on Agency {
                      id
                      name
                      naming
                      __typename
                    }"""

mplan_subfields = """{
                            ...MplanData
                            __typename
                          }
                        }
                        
                        fragment MplanData on Mplan {
                          id
                          orderNo
                          campaign {
                            ...CampaignData
                            __typename
                          }
                          placementsCount
                          status {
                            code
                            name
                            __typename
                          }
                          landings {
                            id
                            url
                            type
                            __typename
                          }
                          conversions {
                            id
                            name
                            __typename
                          }
                          constraints {
                            id
                            metric {
                              name
                              code
                              unit {
                                code
                                name
                                __typename
                              }
                              __typename
                            }
                            operation
                            value
                            __typename
                          }
                          createdAt
                          updatedAt
                          __typename
                        }
                        
                        fragment CampaignData on Campaign {
                          id
                          name
                          status {
                            id
                            name
                            __typename
                          }
                          marketTarget
                          agency {
                            ...AgencyBase
                            __typename
                          }
                          client {
                            id
                            name
                            naming
                            code
                            __typename
                          }
                          coBrands {
                            id
                            name
                            __typename
                          }
                          brand {
                            id
                            name
                            code
                            __typename
                          }
                          product {
                            id
                            name
                            code
                            brands {
                              id
                              name
                              __typename
                            }
                            __typename
                          }
                          department {
                            id
                            __typename
                          }
                          budget
                          startOn
                          finishOn
                          targetAudience
                          conditions
                          createdAt
                          updatedAt
                          status {
                            name
                            code
                            __typename
                          }
                          code
                          documents {
                            id
                            code
                            name
                            path
                            size
                            __typename
                          }
                          approvedMplan {
                            id
                            __typename
                          }
                          isReportReady
                          representative {
                            id
                            name
                            surname
                            middleName
                            __typename
                          }
                          canRepresentativeSetEmpty
                          __typename
                        }
                        
                        fragment AgencyBase on Agency {
                          id
                          name
                          naming
                          __typename
                        }"""

placement_subfields = """{
                                    ...PlacementDataBase
                                    __typename
                                  }
                                }
                                
                                fragment PlacementDataBase on Placement {
                                  id
                                  status {
                                    id
                                    name
                                    code
                                    __typename
                                  }
                                  name
                                  extraNaming
                                  naming
                                  startOn
                                  finishOn
                                  landingURL
                                  timekeeping
                                  budget
                                  project {
                                    id
                                    __typename
                                  }
                                  site {
                                    id
                                    name
                                    shortName
                                    hasAdset
                                    code
                                    naming
                                    url
                                    type
                                    status
                                    publishMethod
                                    canAutoGather
                                    seller {
                                      id
                                      name
                                      naming
                                      code
                                      sources {
                                        id
                                        name
                                        naming
                                        shortName
                                        publishMethod
                                        code
                                        __typename
                                      }
                                      __typename
                                    }
                                    adSizes {
                                      adFormat {
                                        id
                                        name
                                        naming
                                        code
                                        __typename
                                      }
                                      adSize {
                                        id
                                        name
                                        code
                                        __typename
                                      }
                                      __typename
                                    }
                                    buyTypes {
                                      adFormat {
                                        id
                                        code
                                        naming
                                        name
                                        __typename
                                      }
                                      buyType {
                                        id
                                        code
                                        naming
                                        name
                                        __typename
                                      }
                                      __typename
                                    }
                                    __typename
                                  }
                                  channel {
                                    name
                                    code
                                    __typename
                                  }
                                  buyType {
                                    id
                                    name
                                    code
                                    __typename
                                  }
                                  adFormat {
                                    id
                                    name
                                    __typename
                                  }
                                  adSizes {
                                    id
                                    name
                                    __typename
                                  }
                                  createdAt
                                  updatedAt
                                  creativesCount
                                  siteSection {
                                    id
                                    name
                                    naming
                                    __typename
                                  }
                                  siteElement {
                                    id
                                    name
                                    naming
                                    __typename
                                  }
                                  adSystem {
                                    id
                                    name
                                    naming
                                    __typename
                                  }
                                  appsflyerParameter {
                                    id
                                    placementID
                                    retargeting
                                    reEngagementPeriod
                                    attributionWindowPeriod
                                    __typename
                                  }
                                  appsflyerPartner {
                                    id
                                    name
                                    identifier
                                    accountName
                                    adID
                                    __typename
                                  }
                                  platforms
                                  placementType
                                  seller {
                                    id
                                    name
                                    code
                                    __typename
                                  }
                                  __typename
                                }"""


metrics_and_conversions_subfields = """{
                                metrics {
                                  id
                                  metric {
                                    name
                                    code
                                    unit {
                                      name
                                      __typename
                                    }
                                    type
                                    __typename
                                  }
                                  value
                                  isCalculated
                                  __typename
                                }
                                conversionLinks {
                                  id
                                  placementID
                                  mplanConversion {
                                    id
                                    name
                                    __typename
                                  }
                                  isMain
                                  metrics {
                                    id
                                    placementID
                                    value
                                    metric {
                                      name
                                      code
                                      unit {
                                        name
                                        __typename
                                      }
                                      type
                                      __typename
                                    }
                                    isCalculated
                                    __typename
                                  }
                                  __typename
                                }
                                __typename
                              }
                              placements(id: $placementID) {
                                ...PlacementForTargetings
                                __typename
                              }
                              mplans(id: $mediaplanID) {
                                ...MediaPlanForTargetings
                                conversions {
                                  id
                                  name
                                  __typename
                                }
                                __typename
                              }
                            }
                            
                            fragment PlacementForTargetings on Placement {
                              id
                              name
                              naming
                              status {
                                code
                                name
                                __typename
                              }
                              site {
                                name
                                __typename
                              }
                              buyType {
                                name
                                __typename
                              }
                              adFormat {
                                name
                                __typename
                              }
                              adSizes {
                                name
                                __typename
                              }
                              placementType
                              buyType {
                                id
                                code
                                name
                                __typename
                              }
                              __typename
                            }
                            
                            fragment MediaPlanForTargetings on Mplan {
                              id
                              orderNo
                              campaign {
                                id
                                name
                                client {
                                  name
                                  __typename
                                }
                                finishOn
                                startOn
                                __typename
                              }
                              status {
                                code
                                __typename
                              }
                              __typename
                            }"""
reporting_subfields = """{
                                report {
                                  ...ReportFull
                                }
                              }
                            }

                            fragment ReportFull on Report {
                              data {
                                ...ReportDataDeep
                              }
                              meta {
                                dimensions {
                                  ...ReportMetaDimensionDeep
                                }
                                metrics {
                                  ...ReportMetaMetricDeep
                                }
                              }
                            }

                            fragment ReportDataDeep on ReportData {
                              ...ReportDataFlat
                              children {
                                ...ReportDataFlat
                                children {
                                  ...ReportDataFlat
                                  children {
                                    ...ReportDataFlat
                                  }
                                }
                              }
                            }

                            fragment ReportDataFlat on ReportData {
                              dimensions {
                                label
                              }
                              metrics
                            }

                            fragment ReportMetaDimensionDeep on ReportMetaDimension {
                              ...ReportMetaDimensionFlat
                              leafs {
                                ...ReportMetaDimensionFlat
                              }
                            }

                            fragment ReportMetaDimensionFlat on ReportMetaDimension {
                              code
                              label
                              extra
                            }

                            fragment ReportMetaMetricDeep on ReportMetaMetric {
                              ...ReportMetaMetricFlat
                            }

                            fragment ReportMetaMetricFlat on ReportMetaMetric {
                              code
                            }"""
                            
fragment_all_placement = """fragment PlacementForMediaplan on Placement {
                                          id
                                          status {
                                            id
                                            name
                                            code
                                            __typename
                                          }
                                          name
                                          site {
                                            id
                                            name
                                            __typename
                                          }
                                          buyType {
                                            id
                                            name
                                            __typename
                                          }
                                          adFormat {
                                            id
                                            name
                                            __typename
                                          }
                                          channel {
                                            name
                                            code
                                            __typename
                                          }
                                          creativesCount
                                          tools {
                                            type
                                            gatherMethod
                                            publishMethod
                                            __typename
                                          }
                                          updatedAt
                                          budget
                                          __typename
                                        }
                                        """


reporting_digital_connections_subfields = """
                        fragment ReportFull on Report {
                              report {
                                code
                                label
                                __typename
                              }
                              data {
                                ...ReportDataDeep
                                __typename
                              }
                              meta {
                                dimensions {
                                  ...ReportMetaDimensionDeep
                                  __typename
                                }
                                metrics {
                                  ...ReportMetaMetricDeep
                                  __typename
                                }
                                __typename
                              }
                              __typename
                            }
                            
                            fragment ReportDataDeep on ReportData {
                              ...ReportDataFlat
                              children {
                                ...ReportDataFlat
                                children {
                                  ...ReportDataFlat
                                  children {
                                    ...ReportDataFlat
                                    __typename
                                  }
                                  __typename
                                }
                                __typename
                              }
                              __typename
                            }
                            
                            fragment ReportDataFlat on ReportData {
                              dimensions {
                                code
                                label
                                extra
                                __typename
                              }
                              metrics
                              __typename
                            }
                            
                            fragment ReportMetaDimensionDeep on ReportMetaDimension {
                              ...ReportMetaDimensionFlat
                              leafs {
                                ...ReportMetaDimensionFlat
                                __typename
                              }
                              __typename
                            }
                            
                            fragment ReportMetaDimensionFlat on ReportMetaDimension {
                              code
                              label
                              extra
                              __typename
                            }
                            
                            fragment ReportMetaMetricDeep on ReportMetaMetric {
                              ...ReportMetaMetricFlat
                              leafs {
                                ...ReportMetaMetricFlat
                                __typename
                              }
                              __typename
                            }
                            
                            fragment ReportMetaMetricFlat on ReportMetaMetric {
                              code
                              label
                              type
                              extra
                              __typename
                            }
                        """

placement_tools_subfields = """{
                                  ...PlacementToolFragment
                                  __typename
                                }
                              }
                              
                              fragment PlacementToolFragment on PlacementTool {
                                id
                                placementID
                                type
                                gatherMethod
                                publishMethod
                                trackingMethod
                                iToken {
                                  id
                                  __typename
                                }
                                iTool {
                                  id
                                  __typename
                                }
                                apps {
                                  ...PlacementToolApp
                                  __typename
                                }
                                counterID
                                __typename
                              }
                              
                              fragment PlacementToolApp on PlacementToolApp {
                                id
                                applicationID
                                applicationName
                                applicationPlatform
                                inAppEvents
                                __typename
                              }"""

organization_links_subfields = """{
                                        ...OrganizationLink
                                        __typename
                                      }
                                    }

                                    fragment OrganizationLink on OrganizationLink {
                                      id
                                      organization {
                                        id
                                        role
                                        fullName
                                        shortName
                                        firmName
                                        __typename
                                      }
                                      client {
                                        id
                                        name
                                        naming
                                        code
                                        fullName
                                        __typename
                                      }
                                      brand {
                                        id
                                        name
                                        naming
                                        code
                                        __typename
                                      }
                                      product {
                                        id
                                        name
                                        naming
                                        code
                                        __typename
                                      }
                                      __typename
                                    } """