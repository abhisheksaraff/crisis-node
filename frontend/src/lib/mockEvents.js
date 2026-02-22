const minutesAgo = (n) => {
  const date = new Date(Date.now() - n * 60000);
  return date.toISOString();
};
const mockEvents = [
  {
    id: "28344935-2cab-428f-820d-78f2de1d972f",
    type: "earthquake",
    name: "Keeseville, New York, USA",
    lat: 44.5039,
    lng: -73.4829,
    title: "Earthquake reported near Keeseville, NY - WPTZ",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMihAFBVV95cUxNaW1aR1B6VXg1OUV6UzBDLUR5eDJYZ3RFbi1ReXBiUXJ0azYzTEhGbnpsMkQ2aXkyRnJselBRX2FLVUwzN05GaGZwZDdmTDZUTmgtY1JHS2FkNEh2RlRaR1EyZmYwc3JJTW0zREFBTThRdlltbFBmUF82TU1jWXNLenR6MlY?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "WPTZ",
      },
    ],
    details:
      "A seismic event was recorded near Keeseville, NY, on February 16, 2026. The USGS received more than 70 shaking reports from residents in New York and Vermont, specifically between Plattsburgh and Burlington. While initial reports are focused on ground shaking, the situation is being monitored for potential structural damage. Current weather forecasts indicating snow and freezing rain in the region may complicate any necessary field assessments or emergency response activities.",
    actions: [
      {
        done: false,
        task: "Monitor for aftershocks and coordinate with local emergency services to verify reports of structural damage or injuries.",
      },
      {
        done: false,
        task: "Establish communication with local authorities in Plattsburgh and Burlington to ensure situational awareness and identify potential resource gaps.",
      },
      {
        done: false,
        task: "Conduct a rapid assessment of critical infrastructure in the impacted areas to determine if humanitarian assistance is required.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(5),
  },
  {
    id: "4961cd0c-6ce4-43e7-a398-0f0f27e11f87",
    type: "earthquake",
    name: "Irmo, South Carolina, USA",
    lat: 34.086,
    lng: -81.1832,
    title: "Second earthquake in 3 days reported near Irmo - WIS News 10",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMigwFBVV95cUxOcW9PRnNDRnFOb0h3WlBTRnZHNUp5WmFXcUNUUjdYb19kWmpFa045Q0toR2hMa0dEY2UxRXZ6Rnp6VWVxOUNXVVBKTDNrRDZpNEwzRGJ3eWpkWjVMOGxqdnZsZTdHOF9IZXpvUHduUlFFWnI4R3U1VkpaYm9ZUlhXTEJMZw?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "WIS News 10",
      },
    ],
    details:
      "According to the United States Geological Survey, a magnitude 2.0 earthquake occurred approximately three miles west of Irmo, South Carolina. This follows a magnitude 2.8 earthquake on the previous Friday. Local authorities and OCHA are monitoring the situation for potential cluster impacts and structural concerns.",
    actions: [
      {
        done: false,
        task: "Maintain situational awareness and monitor USGS reports for further seismic activity.",
      },
      {
        done: true,
        task: "Coordinate with local emergency management to assess any reported structural damage or community needs.",
      },
      {
        done: false,
        task: "Review and update local contingency plans for seismic events in the region.",
      },
    ],
    is_active: false,
    timestamp: minutesAgo(12),
  },
  {
    id: "4bde59f7-6070-469d-a141-565bc1eacad5",
    type: "flood",
    name: "Topanga Canyon, CA",
    lat: 34.0919,
    lng: -118.6021,
    title:
      "Live weather updates: Flood Watch, evacuation warnings in effect as SoCal storm brings rain - ABC7 Los Angeles",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMi1wFBVV95cUxPakFwWnlBbFJvMnJIdldOeU5pVUdPMWdWYUZ1LWNfWUZaR0tnck1Yc19ZSTJETXlvWFo5N0dIVHhOMTlPOENUY1Vkd0NBcTV4Y1FJVVF6ZU5oUG15eUFlNnhkZ2J6OEVuX1ZKWnhCbk9waDEwSWJjZXlxRzBlU2Q4Zy1GV0lfVTNKSW40c3FDN2Fob19ndmt6dE5ZbE95ejA1ejBRckFqc1VEWjBEUUdLUFNZaU15RkxXeWl3OXZNVzlZeDkzY1pVcTNjMkY0MXZERndtNUxDSQ?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "ABC7 Los Angeles",
      },
    ],
    details:
      "Parts of Topanga Canyon Boulevard were shut down Sunday night ahead of an incoming winter storm, leaving local businesses preparing for disruptions. Officials warn of possible rock slides and debris flows ahead of an incoming winter storm. The roadway is a major connector between the San Fernando Valley and the coast. Officials routinely shut down vulnerable areas when heavy rain is expected. This latest closure stretches from Pacific Coast Highway to Grand View Drive. Residents in burn scar areas are urged to prepare for flooding and debris flows.",
    actions: [
      {
        done: false,
        task: "Enforce evacuation warnings and monitor flood levels in high-risk canyon zones.",
      },
      {
        done: false,
        task: "Establish coordination with Caltrans and local emergency services for road clearing and debris flow management.",
      },
      {
        done: false,
        task: "Perform rapid situational assessments of burn scar areas to identify immediate mudslide risks to residential structures.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(25),
  },
  {
    id: "4efdd4cc-a719-421e-9050-e9a256597e45",
    type: "flood",
    name: "Los Angeles County, CA",
    lat: 34.0522,
    lng: -118.2437,
    title:
      "Cold storm brings rain and threat of flooding. See the rainfall timeline - NBC Los Angeles",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMilgFBVV95cUxQbE9oQ0Q1TmJPZmhObmVmS013d1pMV1lzek9NelhpU3B4bmYxRkplZFJ5QVpYV1FYU0gyNFdYVUVqWU91Zkt0MFoweUpfOHNDc2UyN3RsVVlvZW9ZMUR0M3FvaXBXMXY0OXIxOVJqOTV0b0VnUzNMUGROenRaRWxsbi1pdlVYME4wQXk2ZUd5eGNSc284WGfSAZ4BQVVfeXFMTUNhMjY4NndjLTV3MGFlTDZpb29GQVpSN2xWOXZzRjEzQzg3TTNXZjdSdTgxZFFxeVJCcHpjSlRnM011bUtxZmctR25EcWNvQl8tcEE5QWFJVWFyeVVFRURXRkp4Sy1GNzRVaXJGTUREVHJTel9tZXNURUhJOEhKZDV2V0hMU2JUOFlDc3IrUHJYSlpVYjlTQTFONm1uZFE?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "NBC Los Angeles",
      },
    ],
    details:
      "Flood watches and evacuation warnings are in effect for parts of Los Angeles County as a storm moved into Southern California at the start of a week with several days of wet weather in the forecast. The brunt of the storm is expected Monday with showers early before heavier rain developing in the afternoon. Rainfall totals of 1 to 3 inches in coastal and valley areas and 2 to 5 inches in the mountains are expected. Evacuation warnings are in effect for properties near recent wildfire burn areas including Canyon, Bethany, Eaton, Palisades, Kenneth, Sunset, Lidia, Hurst, Franklin, and Bridge fires zones due to the threat of debris and mud flows.",
    actions: [
      {
        done: false,
        task: "Coordinate with local emergency services to monitor evacuation warning areas in burn scars.",
      },
      {
        done: false,
        task: "Distribute emergency flood safety information and shelter locations to vulnerable communities.",
      },
      {
        done: false,
        task: "Conduct rapid needs assessment for potential debris flow and mudslide impacts in high-risk zones.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(35),
  },
  {
    id: "5990bc8e-c478-4bbd-a78b-13b869925add",
    type: "cyclone",
    name: "Madagascar",
    lat: -18.7669,
    lng: 46.8691,
    title:
      "Cyclone Gezani leaves 59 dead in Madagascar, displaces more than 16,000 - Reuters",

    source: [
      {
        url: "https://news.google.com/rss/articles/CBMiwAFBVV95cUxQU01xMGZnSUN6dkUwQUVaQVpPb2tWQjg4cnRlT3pNRFEtUlRwN0FmRlUzWlFRdXVtUVQ2akhxZGdTeHlxU3FSOHFwTmItQVdvRXUxcnJUeHpSRDlpU2k5a1NrVk0yTE9FX1pWZ2dEZlVHZlJYX3pTXzNTTG15MFNSZTVNa0RMbHdLQzBmWDBGazgwUW03b0x6cTlMMkFCS2hqaTFUUHM2T0V2RzdJTzJKdVU5VHZXTzZIZGQ4eGhVYU4?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "Reuters",
      },
    ],
    details:
      "Cyclone Gezani leaves 59 dead in Madagascar, displaces more than 16,000 Reuters",
    actions: [
      {
        done: false,
        task: "Primary life-saving action: Coordinate emergency search and rescue operations and provide immediate emergency shelter for the 16,000+ displaced individuals.",
      },
      {
        done: false,
        task: "Secondary coordination action: Activate humanitarian clusters, specifically WASH, Food Security, and Health, to ensure coordinated delivery of basic services in affected areas.",
      },
      {
        done: false,
        task: "Tertiary assessment action: Conduct a rapid multi-sectoral needs assessment to provide situational awareness and identify long-term recovery requirements.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(60),
  },
  {
    id: "68fa5b6b-63a3-4261-b75a-494deabe01a6",
    type: "volcano",
    name: "Kilauea Volcano, Big Island, Hawaii",
    lat: 19.4069,
    lng: -155.2833,
    title:
      "UPDATE: Episode 42 of ongoing summit eruption at Kīlauea volcano on Big Island ends after nearly 10 hours - Kauai Now",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMi1AFBVV95cUxOM2hiejJTRGZsUXF6OVRZV2o2bUJvR3VZclZCLTZMR196T0pWWHpIbnR2b2FiY19SMXpmSENzNi02UHlQektBMlhNbmJydDZ2TUppeVV2RDQ3bkxRdzVWQjlGZTRYT0xJXy1wSmpHSzdlaHptQXFrSzI2VXpMSW9acW0tZXVpbGpqM3ZJbHJHYmJKQ19palpRTExZR0RCVllzd2VjakJUQlRVcXh2MGVHNEtVVTlLc3oyOXVWX2J1Z25fZGZRTWI5YzNuWFBWZHBhTmc1Tw?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "Kauai Now",
      },
    ],
    details:
      "Episode 42 of the ongoing Halemaʻumaʻu Crater episodic summit eruption at Kīlauea volcano on the Big Island ended at 11:38 p.m. Sunday (Feb. 15). Tephra fall consisting of fine ash and Pele's hair was reported in Pāhala, Punaluʻu, and Nāʻāehu southwest of Halemaʻumaʻu Crater. While ashfall advisories have been canceled, the potential for minor infrastructure damage and agricultural impact persists due to the episodic nature of the eruption.",
    actions: [
      {
        done: false,
        task: "Monitor for subsequent eruptive episodes and maintain situational awareness with the Hawaiian Volcano Observatory.",
      },
      {
        done: false,
        task: "Coordinate with local agricultural and environmental clusters to assess impact on crops and livestock from tephra fall.",
      },
      {
        done: false,
        task: "Evaluate minor infrastructure and equipment damage in areas southwest of Halemaʻumaʻu Crater.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(90),
  },
  {
    id: "af6b9245-eb3b-4286-978b-f2ae3652309b",
    type: "wildfire",
    name: "Texas, USA",
    lat: 31.9686,
    lng: -99.9018,
    title:
      "Gov. Abbott activates more state wildfire response resources - KWKT - FOX 44",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMingFBVV95cUxQcWVmSWJjZ3hEMTc2b0JMVThsY1VlaU1GUDhRU21lNUY5WU1NSXNWalJHZ0VvMVpGNFB4eVVBOElOMW0zMjdLczFiV2tqYlNYbF9PdWhSTlJ0T1J4UDVNSHBQdXZ0Qnd2eEt3Q29Nc2pSYURyai1Bc2FfakhrNktCSHMtQ3NkWml5TmNiVFZkcHBVTkFOZXJIUk9WYXhMd9IBowFBVV95cUxNNGdhalBlZTZBNjVoTlFGZjZfSUdYWExBMWxJWWlaT0VUM3BaMkdaaFQydDdfMm5RYW1EdWF2M2s0dmQ2TlhvSGJjSmVxNmh2VUN2V3Rhc2FmQl9yVEpDSUJhemx4THhmWnR3S3JFQzVtZjVSd05vOGlPNTZRMGYxVEVvdUNMSE1memVUMzNXZl9NWDZyc2M5VUxOS2U4Wlg4c0tV?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "KWKT - FOX 44",
      },
    ],
    details:
      "Gov. Abbott activates more state wildfire response resources KWKT - FOX 44",
    actions: [
      {
        done: false,
        task: "Immediate evacuation of at-risk communities and deployment of firefighting assets to contain the wildfire spread.",
      },
      {
        done: false,
        task: "Establish an Emergency Operations Center (EOC) to coordinate between state agencies and local emergency services.",
      },
      {
        done: false,
        task: "Conduct rapid aerial and ground assessments to determine the extent of damage and identify immediate humanitarian needs for displaced populations.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(150),
  },
  {
    id: "c0be9e8f-144f-44c8-aa64-5e2ba8b835ab",
    type: "cyclone",
    name: "East Coast, USA",
    lat: 41.0762,
    lng: -73.8587,
    title:
      "Winter storm may intensify and hit East Coast as bomb cyclone - AOL.com",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMif0FVX3lxTE1pQTQ0UDdpbVpOdFdwdk5JV0lPV1BQOTlJMjdleV9BUXczNjRuYWFoMFlzR3RSNDNwUHRIYXJVNE9mNDRWUFpTR3Z0UWJtcVRCc3ZKYTEtRnd0Skp5ZzJrZmhQQUxQOG9Bc3dZcVN5THVydjYwZ1o3NnV4ekJqbFk?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "AOL.com",
      },
    ],
    details:
      "Much of the East Coast is on high alert for another potentially powerful winter storm. A weekend storm could intensify into a 'bomb cyclone,' with the potential for significant snow, strong winds and some coastal flooding from the Carolinas to New England, including areas still recovering from last weekend's snow and ice storm. The National Weather Service indicates heavy snow potential and coastal flooding threats due to high winds and waves. Major impacts are expected, causing considerable disruptions to daily life.",
    actions: [
      {
        done: false,
        task: "Coordinate with local emergency services and FEMA for search and rescue and emergency shelter provision for at-risk populations.",
      },
      {
        done: false,
        task: "Activate Emergency Telecommunications and Logistics clusters to ensure maintain communication lines and supply chains for essential goods.",
      },
      {
        done: false,
        task: "Conduct rapid post-storm needs assessments to evaluate infrastructure damage and identify recovery requirements for affected communities.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(180),
  },
  {
    id: "edbd5de2-9f61-4070-886c-91184b170019",
    type: "volcano",
    name: "Kilauea Volcano, Hawaii",
    lat: 19.4069,
    lng: -155.2833,
    title: "Hawaii's Kilauea volcano erupts - The Guardian",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMilAFBVV95cUxPTTVlX0MwcjJXMUoyRUpIcWJwcm9qRnZnYXoxajZUcllqTUhtbW8wLTdzQm1IMFB3YW5pZHpRMmxDblc3cnVpWWtrQ2x0a3k0RVBRSC1yM3JtZW44ZXVoTkRKRG9pV0dzR045cUR5VHFHa2dDWXJZb2lpazRWNWJSd3JqMS14VTJneXZnTmU3b2Q3LTZ0?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "The Guardian",
      },
    ],
    details:
      "The Kilauea volcano in Hawaii erupted on Sunday, sending lava fountains, ash and smoke into the air. The US Geological Survey said it was the 42nd episode of lava fountains since the current series of intermittent eruptions began in December 2024. The plume from the latest eruption reached more than 10,000 metres (35,000 feet), according to the National Weather Service.",
    actions: [
      {
        done: false,
        task: "Primary life-saving action: Issue immediate safety advisories for volcanic ash and tephra fall to affected communities.",
      },
      {
        done: false,
        task: "Secondary coordination action: Coordinate with the aviation cluster to assess risks and manage air traffic safety due to high-altitude ash plumes.",
      },
      {
        done: false,
        task: "Tertiary assessment action: Conduct a situational awareness assessment of potential health impacts and infrastructure damage from volcanic gases.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(240),
  },
  {
    id: "fee63439-c188-49ff-8041-0c052af646ab",
    type: "wildfire",
    name: "Eastern New Mexico, USA",
    lat: 34.5199,
    lng: -105.8701,
    title: "Xcel Energy prepares for wildfire risk, outages - KOAT",
    source: [
      {
        url: "https://news.google.com/rss/articles/CBMihwFBVV95cUxNRHdGck1WRXdkZEJpakZ0cXNFYlNaa3B0bFpxdjNkX2d1eDZ1a2JyRlUwZzllRHVpTjI3ZWk4TFFtamFMSVlSdzRNbFFOWTFudFRhRE1CSE90SjV4Y3h1VXQxMzNHalJiVlhxaTNXaWJuQldvNWRTbkxxVUhfd013TzdlcHkyZ0E?oc=5&hl=en-CA&gl=CA&ceid=CA:en",
        name: "KOAT",
      },
    ],
    details:
      "Xcel Energy is preparing for heightened wildfire risk in eastern New Mexico, warning customers that a Public Safety Power Shutoff (PSPS) may be necessary Tuesday, Feb. 17. Unseasonably warm, dry conditions, combined with high winds and parched vegetation, have increased the likelihood of wildfires. Enhanced Powerline Safety Settings will be active to automatically shut off lines if hazards are detected. OCHA is monitoring the situation for potential humanitarian impacts, particularly for vulnerable populations dependent on electrically powered medical equipment.",
    actions: [
      {
        done: false,
        task: "Coordinate with local emergency management and fire services to maintain situational awareness and readiness for potential evacuations.",
      },
      {
        done: false,
        task: "Identify and support vulnerable populations requiring backup power for medical equipment through health cluster coordination.",
      },
      {
        done: false,
        task: "Establish communication protocols with utility providers and local authorities to monitor power outage impacts on essential services.",
      },
    ],
    is_active: true,
    timestamp: minutesAgo(300),
  },
];

export default mockEvents;
