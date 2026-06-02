#!/usr/bin/env python3
"""
Phase 4A: Document Collection and Batch Indexing
Generates and indexes a collection of defence documents
"""

import sys
import os
import time
import logging
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_defence_documents():
    """Generate a collection of realistic defence documents"""
    
    documents = []
    
    # ===== BUDGET & FINANCIAL DOCUMENTS =====
    budget_docs = [
        {
            "title": "Defence Budget Analysis FY2024-25: Resource Allocation and Priorities",
            "document_type": "Financial Report",
            "content": """The Defence Budget for FY2024-25 represents a significant allocation of resources toward modernization 
and strategic readiness. This comprehensive financial analysis examines how defence resources are allocated across multiple strategic 
priorities. Key allocations include: Personnel costs (45%), Equipment procurement (30%), Research and Development initiatives (15%), 
Infrastructure development (10%). The budget prioritizes emerging technologies including artificial intelligence integration, 
cyber defence capabilities, and space-based surveillance systems. The allocation breakdown across services includes: 
Army 40% (primarily for land-based modernization), Navy 25% (focused on carrier task forces and submarine development), 
Air Force 30% (concentrated on fighter aircraft and indigenous platform development), and Other specialized agencies 5%.

Major procurement focuses include indigenous platforms to reduce import dependency and boost domestic defence manufacturing. 
The government has allocated ₹10,000 crores specifically for indigenous platform development including fighter jets, 
missiles, and naval vessels. This strategic shift aims to achieve 60% self-reliance in defence equipment by 2030, 
reducing foreign exchange outflows and creating high-skilled manufacturing jobs across the country.

Personnel-related expenditure covers salaries, pensions, and benefits for 2.2 million active and retired defence personnel. 
The budget includes provisions for improved living standards, modernized medical facilities, and enhanced training programs. 
Equipment procurement emphasizes next-generation platforms with integrated sensors, advanced avionics, and network-centric warfare capabilities.

Research and Development initiatives focus on hypersonic technologies, quantum computing applications, and AI-based autonomous systems. 
Infrastructure development includes construction of new strategic bases, runway extensions for heavier aircraft operations, 
and advanced maintenance facilities. The budget projection shows 8-12% annual growth in defence spending over the next decade, 
aligning with strategic modernization requirements and emerging geopolitical challenges in the Indo-Pacific region."""
        },
        {
            "title": "Long-Term Fiscal Planning for Defence Infrastructure (2024-2034)",
            "document_type": "Strategic Document",
            "content": """This comprehensive ten-year fiscal roadmap guides defence infrastructure development and strategic investment. 
Capital expenditure projections demonstrate steady 8-10% annual growth in modernization budget allocation, ensuring sustained 
technological advancement and operational readiness. Strategic investment priorities include: coastal defence infrastructure enhancement, 
critical border area development, state-of-the-art technology innovation hubs, and world-class training and testing facilities.

Investment in human capital development is recognized as crucial for maintaining competitive advantage in modern warfare. 
The roadmap allocates ₹8,000 crores for personnel training infrastructure, officer development academies, and specialized warfare training centers. 
Infrastructure projects span across 15 states with estimated full completion by 2032. Major project categories include naval shipyards 
capable of indigenous platform construction, air force bases with extended runways for next-generation aircraft, 
and army cantonment areas with cutting-edge facilities.

Expected GDP contribution from defence manufacturing sector is projected at 2.5-3%, creating approximately 500,000 direct 
manufacturing jobs and 1.5 million indirect employment opportunities. The fiscal plan emphasizes technology transfer from allied nations, 
establishing joint ventures with defence contractors, and building an ecosystem of Tier-1 and Tier-2 defence suppliers. 
Regional distribution ensures balanced development across economically underdeveloped areas while maintaining strategic accessibility to borders.

Infrastructure modernization includes smart base development with IoT-enabled systems, centralized logistics management, 
and renewable energy integration. Environmental sustainability measures are incorporated with targets for carbon neutrality 
in military operations by 2050. International partnerships in infrastructure development strengthen defence capabilities 
while building strategic relationships with key allied nations."""
        },
        {
            "title": "Cost-Benefit Analysis of Indigenous Weapons Platform Development",
            "document_type": "Economic Analysis",
            "content": """Comprehensive comparative study of indigenous versus imported defence platforms with detailed cost-benefit analysis. 
Indigenous platform development reduces foreign exchange outflow by approximately 60-70%, translating to significant savings 
in India's balance of payments position. Long-term strategic benefits include technology sovereignty, job creation across manufacturing sectors, 
export opportunities in global defence markets, and reduced vulnerability to sanctions or political pressure from supplier nations.

Development timelines based on historical data and international benchmarks: fighter aircraft approximately 8 years from conceptualization 
to initial operational capability, missile systems 5 years, naval vessels 6 years for design and first platform. Cost estimates for major platforms: 
fighter aircraft development ₹4,500 crores per platform class, missile system programs ₹800-1,200 crores, destroyer-class naval vessels ₹3,000-3,500 crores.

Employment generation through indigenous defence manufacturing is substantial: 50,000+ direct manufacturing jobs, 150,000+ indirect employment 
opportunities in supporting industries, and 100,000+ jobs in R&D, testing, and certification facilities. Skill development initiatives train workers 
in advanced manufacturing techniques, composite materials production, and precision engineering. Regional economic development benefits include 
technology spillovers to civilian industries, research facility development, and infrastructure improvements in defence manufacturing hubs.

Comparative analysis with international platforms shows that indigenous development, while requiring higher initial investment, 
provides better long-term value through reduced operational costs, localized support infrastructure, and customization capability. 
Technology transfer agreements with strategic partners accelerate development timelines while maintaining operational security. 
Licensing production of selected international platforms supports domestic manufacturing capabilities and technology absorption."""
        },
    ]
    documents.extend(budget_docs)
    
    # ===== STRATEGIC & POLICY DOCUMENTS =====
    strategy_docs = [
        {
            "title": "National Defence Strategy 2024-2035: Grand Strategy Framework",
            "document_type": "Strategic Document",
            "content": """The comprehensive national defence strategy addresses emerging threats in the Indo-Pacific region while establishing 
a framework for sustained military modernization. Core strategic pillars include: (1) Strategic autonomy in key technologies including semiconductors, 
rare earth minerals, and critical defence systems, ensuring independence from supply chain vulnerabilities; (2) Regional stabilization through credible 
deterrence capabilities across air, naval, and land domains; (3) Economic-military integration creating synergies between defence manufacturing 
and broader economic development.

Identified threat assessment encompasses: cross-border terrorism originating from non-state actors, cyber warfare capabilities targeting critical 
infrastructure, space-based threats including anti-satellite weapons, and climate-induced security challenges affecting resource availability 
and population displacement. The strategy recognizes asymmetric warfare as primary threat requiring different operational approaches than 
conventional conflict scenarios.

Strategic partnerships with allied nations prioritize India-US deep defence cooperation, India-Japan coordination in maritime security, 
India-Australia collaboration in Indo-Pacific stability, and Vietnam partnership for regional balance. Defence posture balances offensive capabilities 
in precision strike systems with defensive resilience in air defence and cyber protection. Military modernization targets 175 warships, 
240 combat aircraft, and world-class sensor networks providing real-time situational awareness across entire operational domain.

The strategy emphasizes technology advancement in autonomous systems, artificial intelligence applications, quantum computing for cryptography, 
and advanced materials for platform development. Doctrinal evolution moves toward integrated theatre operations with network-centric warfare capabilities, 
precision munitions, and sensor-to-shooter systems reducing engagement timelines significantly. Manpower planning focuses on quality over quantity, 
with emphasis on professional competency and advanced training."""
        },
        {
            "title": "Joint Theatre Command Implementation Roadmap",
            "document_type": "Strategic Document",
            "content": """Implementation framework for establishing unified theatre commands as proposed by the Chief of Defence Staff. 
This transformational reorganization consolidates geographical and functional commands under single theatre commander, 
creating streamlined command structures with unified planning and execution authorities. Theatre commands include: Western Theatre (India-Pakistan border), 
Northern Theatre (China border, high altitude operations), Eastern Theatre (Bangladesh-Myanmar region), Maritime Theatre (Indian Ocean), 
Cyber Theatre (digital warfare operations), Space Theatre (satellite operations and space defence).

Expected efficiency gains from unification: 15-20% reduction in administrative overhead and redundant support structures, faster decision-making cycles 
through simplified command chains, improved inter-service coordination eliminating compartmentalization, and better resource optimization. 
Transition timeline structured in three phases: Phase 1 (2024-25) establishes new command structures with compatible organizational frameworks; 
Phase 2 (2025-26) implements resource consolidation with integrated logistics and personnel management; Phase 3 (2026-27) achieves full operationalization 
with theatre-level integrated exercises demonstrating seamless inter-service coordination.

Risk mitigation strategies address potential institutional disruption through: smooth transition protocols minimizing operational gaps, 
comprehensive training programs for officers and support staff adapting to new command structures, maintenance of continuity during transition period, 
and retention mechanisms for experienced personnel. Technology integration includes unified command and control systems, real-time data sharing across services, 
and AI-based decision support systems providing situational assessment and recommendation synthesis.

Performance metrics for successful theatre command implementation include reduced decision-making timelines, improved operational effectiveness metrics, 
enhanced inter-service coordination demonstrated through joint exercises, and cost optimization targets. The transformation represents major institutional 
change requiring sustained commitment from military leadership, government support, and international partnerships with allied nations having similar structures."""
        },
        {
            "title": "Maritime Security Strategy for Indian Ocean Region",
            "document_type": "Policy Document",
            "content": """Comprehensive maritime security framework encompassing 3.7 million square kilometers of maritime zone under Indian jurisdiction. 
Strategic objectives for maritime operations include: freedom of navigation protection ensuring international shipping lanes remain open and secure, 
advanced anti-piracy operations leveraging satellite surveillance and naval patrol assets, counter-terrorism at sea targeting maritime militant groups, 
and environmental monitoring protecting marine ecosystems and detecting illegal activities. The maritime security strategy recognizes India's 
critical economic dependence on sea lanes with 95% of external trade conducted through maritime routes.

Naval force modernization roadmap targets achieving 175 operational ships by 2035, with current fleet strength at 140 vessels. Major construction programs 
include Project 15B destroyers (advanced sensor systems and guided missiles), Project 17A frigates (multi-role combat capability), Project 75I submarines 
(enhanced underwater warfare capability), and fleet support vessels. Submarine capability expansion encompasses 24 total submarines including 6 nuclear-powered 
ballistic missile submarines (SSBNs) providing strategic deterrence and 4 nuclear-powered attack submarines (SSNs) for power projection.

Advanced surface platforms modernization includes carrier task forces with INS Vikrant-class aircraft carriers (indigenous development), 
naval aviation modernization with MiG-29K fighters and advanced helicopters, and integrated air defence systems providing layered protection. 
Naval aviation expansion includes 100+ naval helicopters and 200+ maritime patrol aircraft distributed across operational commands. 
Regional cooperation through the SAGAR (Security and Growth for All in the Region) initiative strengthens maritime security partnerships, 
while participation in Indian Ocean Rim Association enables coordinated responses to transnational maritime challenges.

Strategic chokepoints receive special attention with enhanced surveillance capabilities and rapid response forces, particularly Strait of Malacca, 
Strait of Hormuz, and other critical waterways. Technology integration includes satellite-based ocean surveillance, real-time intelligence fusion, 
and automated threat detection systems. Cyber maritime operations address emerging threats to port infrastructure and vessel navigation systems."""
        },
        {
            "title": "Cyber Defence Architecture and National Digital Resilience Plan",
            "document_type": "Technical Strategy",
            "content": """Multi-layered cyber defence architecture protects critical defence infrastructure, government networks, and national 
security installations against sophisticated cyber attacks. Establishment of National Cyber Security Centre with 24/7 monitoring capabilities 
provides continuous threat detection, rapid response activation, and incident management. Threat detection capabilities target nation-state level attacks, 
organized cyber criminal groups, and individual hackers, with machine learning systems identifying novel attack patterns and zero-day exploits.

Integration with civil agencies including CERT-In, intelligence agencies, and critical infrastructure operators creates coordinated response mechanisms. 
The architecture incorporates multiple security layers: perimeter defence with advanced firewalls and intrusion detection systems, internal segmentation 
isolating critical systems, endpoint protection on all connected devices, and application-level security. Training of 10,000 cyber warriors annually 
builds indigenous cyber workforce capability reducing dependence on foreign expertise.

Investment in indigenous cybersecurity solutions reduces vendor dependency and protects sensitive military information from potential backdoors 
in foreign software. Collaboration with academia establishes cyber research centers, develops advanced security technologies, and creates talent pipeline 
for continuous workforce expansion. Cyber defence budget allocation of ₹5,000 crores over 5 years supports infrastructure development, training programs, 
and advanced technology acquisition.

Specific focus areas include: encryption system development ensuring unhackable communications, AI-based intrusion detection identifying sophisticated attacks, 
quantum computing preparation developing post-quantum cryptography, and supply chain security ensuring no compromised components enter defence systems. 
International partnerships with allied nations strengthen collective cyber defence posture through information sharing and coordinated response protocols. 
Offensive cyber capabilities provide deterrence and retaliatory options against hostile cyber operations. Regular cyber war games and simulation exercises 
maintain readiness and identify capability gaps."""
        },
    ]
    documents.extend(strategy_docs)
    
    # ===== OPERATIONAL & TACTICAL DOCUMENTS =====
    operational_docs = [
        {
            "title": "Counter-Terrorism Operations Manual and Best Practices",
            "document_type": "Operational Manual",
            "content": """Comprehensive operational guidelines for counter-terrorism missions across diverse geographical and operational contexts. 
Integration of intelligence, surveillance, and reconnaissance capabilities with tactical operations provides real-time situational awareness. 
Rules of engagement emphasizing civilian protection and proportionality ensure operations comply with international humanitarian law. 
Standard operating procedures adapted for different terrain types: mountainous regions like Kashmir and Northeast with elevation challenges, 
urban environments in metro areas with civilian density considerations, and riverine operations in wetland areas.

Training requirements specify 500+ hours for frontline operators covering weapons handling, tactical movement, hostage rescue techniques, 
and cultural awareness. Support personnel require 200+ hours training in logistics, communications, and medical support. Technology deployment 
includes unmanned aerial vehicles for surveillance, secure communication systems with encryption, and real-time intelligence fusion systems. 
Success metrics include 95%+ mission completion rate, civilian casualty minimization, and efficiency in intelligence gathering.

Specialized operations training covers mountaineering and altitude acclimatization, urban close-quarter combat, helicopter insertion techniques, 
and underwater operations. Equipment standards specify precision rifles, advanced body armor, night vision systems, and thermal imaging capabilities. 
Command and control protocols establish clear chains of authority, abort decision criteria, and coordination procedures. After-action reviews 
systematically capture lessons learned and identify capability improvements. International training exchanges with allied nations provide exposure 
to different operational approaches and best practices. Counter-terrorism doctrine continues evolving based on threat analysis and emerging tactics."""
        },
        {
            "title": "Border Management and Coastal Security Operations Manual",
            "document_type": "Operational Document",
            "content": """Standard procedures for comprehensive management of 15,106 kilometers of land border and 7,517 kilometers of coastline. 
Surveillance infrastructure encompasses 2,500+ surveillance cameras, comprehensive sensor networks, and real-time satellite imagery feeds. 
Personnel deployment across all borders totals 500,000+ trained personnel providing continuous presence and rapid response capability. 
Technology integration includes automated threat detection systems, unmanned drone patrols with extended flight endurance, and sensor fusion 
systems correlating multiple data sources for threat identification.

Coordination mechanisms link Border Security Force, Coast Guard, state police, and military units through unified command structures. 
Cross-border incident protocols establish communication channels, rules for engagement, de-escalation procedures, and escalation pathways 
for different threat levels. Coastal security operations deploy 500+ interceptor boats, naval vessels with advanced weapons systems, and 
aircraft providing surveillance and rapid response. Infrastructure security measures protect strategic ports, naval facilities, and critical 
communication installations from sabotage and terrorism.

Personnel training covers border patrolling techniques, threat recognition protocols, communication procedures, and emergency response. 
Environmental monitoring identifies unusual activities including smuggling operations, infiltration attempts, and illegal maritime activities. 
Technology provides early warning of aerial threats, vehicular movement detection, and precision identification of crossing points. 
Intelligence sharing with international partners including Bangladesh, Myanmar, and Pakistan reduces transnational criminal activity. 
Statistics tracking monitors penetration attempts, interdiction rates, and incident patterns informing continuous operational improvements."""
        },
        {
            "title": "Joint Military Exercise Planning and Conduct Framework",
            "document_type": "Operational Guidelines",
            "content": """Framework for planning and conducting joint military exercises. Exercises classified: HADR (humanitarian), 
bilateral, multilateral, live-fire, tabletop. Annual exercise calendar: 50+ exercises across all services. Exercise evaluation metrics: 
readiness assessment, inter-service coordination, technology validation, personnel training. Resource requirements and logistics planning. 
International participation protocols. Post-exercise analysis and lessons learned documentation. Participation costs: ₹500 crores annually."""
        },
    ]
    documents.extend(operational_docs)
    
    # ===== MODERNIZATION & EQUIPMENT DOCUMENTS =====
    modernization_docs = [
        {
            "title": "Indigenous Fighter Aircraft Development: HAL Tejas Mark II Specifications",
            "document_type": "Technical Report",
            "content": """HAL Tejas Mark II fifth-generation fighter development specifications. Performance parameters: 
Max speed Mach 2.0, service ceiling 18,000 m, combat radius 3,000 km. Armament: 12 hardpoints for missiles and weapons. 
Advanced AESA radar with 250 km detection range. Engine options: GE F414 or indigenous Kaveri derivative. Digital cockpit with 
AI-assisted decision support. Stealth features reducing RCS by 65% compared to Mark I. First flight expected 2026, IOC 2028. 
Total program cost: ₹50,000 crores for 200 aircraft."""
        },
        {
            "title": "Guided Missile Development Program: Brahmos and Beyond",
            "document_type": "Technical Document",
            "content": """Comprehensive overview of India's guided missile arsenal. Brahmos: supersonic cruise missile, range 300+ km, 
speed Mach 3+. Akash: air defence system, range 30 km, altitude coverage 15,000 m. Astra: beyond visual range air-to-air missile, 
range 100+ km. Nirbhay: long-range cruise missile, range 1,000+ km. Next-generation programs: hypersonic cruise missile development, 
quantum radar integration, AI-guided targeting. Annual missile test schedule: 20+ tests. Production capacity: 500+ missiles annually 
from multiple production facilities."""
        },
        {
            "title": "Naval Modernization: INS Vikrant Class Carrier Development",
            "document_type": "Technical Specification",
            "content": """Development of indigenous aircraft carrier, INS Vikrant (40,000 tonnes). Specifications: 260 m length, 
62 m beam, flight deck accommodating 30+ aircraft. Propulsion: 2x 9MW gas turbines, speed 18 knots. Complement: 1,600 personnel. 
Advanced AESA radar and integrated air defence. Aircraft complement: MiG-29K, naval helicopters, drones. Production timeline: 
first carrier commissioned 2023, second under construction. Technology transfer agreements with France and Russia for advanced systems. 
Total program value: ₹40,000 crores for two carriers."""
        },
        {
            "title": "Army Modernization: Future Soldier Integrated Combat System",
            "document_type": "Technology Document",
            "content": """Comprehensive soldier modernization program integrating technology with combat effectiveness. System components: 
advanced body armor (10mm ceramic plates), smart helmet with integrated communication, thermal imaging, AR display, night vision. 
Weapon systems: modular assault rifles (5.56mm/.30-06 capability), advanced fire control systems. Logistics: integrated supply chain, 
AI-predicted demand, drone-based resupply. Training: VR-based combat simulation, AI tutoring systems. Deployment timeline: 20,000 
soldiers equipped by 2025, full army by 2030. Cost per soldier: ₹50 lakhs for complete system."""
        },
    ]
    documents.extend(modernization_docs)
    
    # ===== TRAINING & PERSONNEL DOCUMENTS =====
    training_docs = [
        {
            "title": "Defence Forces Training and Professional Development Curriculum",
            "document_type": "Training Document",
            "content": """Comprehensive training curriculum for defence personnel across ranks and specializations. 
Officer training: 3-year National Defence Academy, followed by service-specific training. Enlisted training: 6-18 months depending on specialization. 
Specialization tracks: combat arms, technical specializations, logistics, intelligence, cyber operations, space operations. 
Continuous professional development: 100+ hours annually for all personnel. International training exchanges with 15+ countries. 
Advanced course offerings: higher defence management, strategic studies, space technology. Training infrastructure: 200+ establishments, 
50,000+ annual training capacity."""
        },
        {
            "title": "Leadership Development and Officer Professionalisation Strategy",
            "document_type": "Strategic Document",
            "content": """Strategy for developing military leadership aligned with modern warfare requirements. 
Officer development pathway: NDA → service academy → junior command courses → advanced command courses → higher defence management. 
Emphasis on civil-military interface, strategic thinking, and technology understanding. International exposure: staff college exchanges, 
advanced training in allied nations. Mentorship programs pairing senior and junior officers. Leadership training budget: ₹2,000 crores 
annually. Target: 100% officers with advanced professional qualifications by 2030."""
        },
        {
            "title": "Women in Defence Forces: Integration and Capability Enhancement",
            "document_type": "Policy Document",
            "content": """Comprehensive policy for women's integration across defence forces. Target: 20% women personnel by 2032 (currently 4%). 
Roles opened: combat positions, technical specializations, command positions, all-women units. Training adaptations: equipment sizing, 
facility design, curriculum modifications. Support systems: childcare facilities, flexible deployment options, mentorship programs. 
Annual recruitment: 5,000+ women across all services. Retention rate: 95%+ with improved career progression. Budget allocation: ₹5,000 
crores for infrastructure and support systems."""
        },
    ]
    documents.extend(training_docs)
    
    # ===== RESEARCH & TECHNOLOGY DOCUMENTS =====
    research_docs = [
        {
            "title": "Artificial Intelligence Integration in Defence Systems: Strategic Roadmap",
            "document_type": "Research Document",
            "content": """Strategic roadmap for AI integration across defence operations. Applications: autonomous vehicles and drones, 
predictive maintenance, intelligence analysis, cyber defence, logistics optimization. Investment: ₹10,000 crores over 5 years for R&D. 
Research focus areas: computer vision for target detection, natural language processing for intelligence analysis, reinforcement learning 
for tactical planning. Partnership with IIT, CSIR, and private tech companies. Ethical guidelines: human-in-loop for lethal decisions, 
transparency in algorithms, bias detection. Expected capability enhancement: 30-40% operational efficiency improvement."""
        },
        {
            "title": "Space-Based Defence Capabilities: Surveillance and Communication Infrastructure",
            "document_type": "Technology Strategy",
            "content": """Development of space-based defence infrastructure for surveillance and communication. Satellite constellation: 
10+ earth observation satellites, 5+ communication satellites deployed over 5 years. Resolution: sub-meter for critical areas. Coverage: 
real-time monitoring of 3.7M sq. km maritime zone, 15,106 km borders. Anti-satellite capability development: indigenous ASAT systems. 
Space debris tracking and mitigation. Space operations command establishment. Budget: ₹15,000 crores over 10 years. Strategic autonomy 
in space access by 2030."""
        },
        {
            "title": "Quantum Technology Applications in Defence: Encryption and Sensing",
            "document_type": "Research Initiative",
            "content": """Exploration of quantum technologies for defence applications. Focus areas: quantum key distribution for unhackable 
communication, quantum sensors for enhanced detection capabilities, quantum computing for cryptanalysis resistance. R&D partnerships with 
quantum tech startups and research institutions. Prototype development timeline: 2-3 years for QKD systems, 4-5 years for quantum sensors. 
Investment: ₹5,000 crores. Expected capability: quantum-resistant communication by 2027, operational quantum sensors by 2030. Technology 
sovereignty ensuring no backdoors or foreign dependencies."""
        },
    ]
    documents.extend(research_docs)
    
    # ===== GEOPOLITICAL & SECURITY DOCUMENTS =====
    geopolitical_docs = [
        {
            "title": "Indo-Pacific Security Assessment: Strategic Implications and Response",
            "document_type": "Strategic Assessment",
            "content": """Assessment of security dynamics in Indo-Pacific region with implications for India. Key actors: China, US, Japan, 
Australia, Vietnam, Southeast Asian nations. Threat assessment: power projection capabilities, territorial claims, militarization. 
Strategic opportunities: Quad cooperation, bilateral partnerships, regional influence. India's role: balancing power, maintaining freedom 
of navigation, supporting regional stability. Military capabilities required: enhanced naval presence, extended strike range, air superiority 
in regional airspace. Proposed actions: 15-aircraft carrier task forces, submarine fleet expansion, advanced air defence systems."""
        },
        {
            "title": "Border Security Assessment: China and Pakistan Threats",
            "document_type": "Security Document",
            "content": """Comprehensive assessment of threats from land borders with China and Pakistan. LAC issues: border skirmishes, 
infrastructure development, military posturing. PAK border: cross-border terrorism, infiltration attempts, artillery attacks. 
Current threat levels: HIGH (both borders). Military response measures: enhanced personnel deployment, advanced surveillance systems, 
rapid response capabilities, border infrastructure development. Technology deployment: sensor networks, radar coverage, drone surveillance. 
Investment in border area development: ₹10,000 crores for infrastructure. Projected force strength: 1.2M personnel by 2030."""
        },
        {
            "title": "Terrorism and Internal Security Challenges: Counter-Measures Strategy",
            "document_type": "Security Strategy",
            "content": """Counter-terrorism and internal security strategy addressing multiple fronts. Terror threat assessment: 
cross-border sponsored terrorism, left-wing extremism, communal violence, insurgency. Prevention measures: intelligence gathering, 
predictive policing, community engagement. Operational response: specialized counter-terrorism units, rapid reaction forces, precision 
operations. Technology deployment: surveillance systems, AI-based threat detection, secure communication. Budget allocation: ₹20,000 
crores annually. Coordination between military, paramilitary, and civil agencies. Expected outcome: 40% reduction in terror incidents 
by 2027."""
        },
    ]
    documents.extend(geopolitical_docs)
    
    # ===== DEFENSE PARTNERSHIPS & INTERNATIONAL DOCUMENTS =====
    international_docs = [
        {
            "title": "India-USA Defence Partnership: Strategic Alignment and Cooperation Framework",
            "document_type": "Partnership Document",
            "content": """Comprehensive framework for India-USA defence cooperation. Key agreements: Logistics Exchange Memorandum of Agreement 
(LEMOA), Communications Compatibility and Security Agreement (COMCASA), Basic Exchange and Cooperation Agreement (BECA). 
Military-to-military engagement: joint exercises annually, personnel exchanges, training programs. Technology transfer: co-development 
of advanced systems, access to emerging technologies, shared R&D initiatives. Defense trade: $20+ billion in potential defence procurement. 
Strategic alignment: Indo-Pacific security, counter-terrorism, maritime security. Planned activities: 10+ annual joint exercises, 
200+ military exchanges annually."""
        },
        {
            "title": "India-Japan Defence Cooperation: East Asia Security Initiative",
            "document_type": "Bilateral Agreement",
            "content": """India-Japan defence partnership strengthening regional security. Joint exercises: annual naval exercises, 
air force coordination, ground forces interaction. Technology cooperation: surveillance systems, naval platforms, defence manufacturing. 
Cost-sharing: 50-50 partnership model. Strategic objectives: regional stability, freedom of navigation, counter-terrorism. QUAD cooperation 
integration: coordinated actions with USA and Australia. Military exchange programs: 100+ personnel annually. Joint R&D: indigenous platform 
development, cyber defence systems. Investment target: $15 billion over 10 years."""
        },
        {
            "title": "Regional Military Dialogue and SAARC Defence Initiatives",
            "document_type": "Regional Framework",
            "content": """Framework for regional dialogue and cooperation within SAARC and broader South Asia. Confidence building measures: 
military-to-military hotlines, incident communication protocols, joint disaster response drills. Regional stability initiatives: 
anti-terrorism coordination, maritime security cooperation, peacekeeping participation. Training programs: 500+ regional military personnel 
annually. Joint research: climate-induced security challenges, disaster management, technology sharing. Annual dialogue forums: defence 
ministers meeting, military expert working groups. Budget: ₹500 crores annually for regional initiatives."""
        },
    ]
    documents.extend(international_docs)
    
    # ===== SPECIAL OPERATIONS & INTELLIGENCE DOCUMENTS =====
    special_docs = [
        {
            "title": "Special Operations Forces: Organization and Capability Development",
            "document_type": "Operational Document",
            "content": """Organization and capability framework for special operations forces. Units: Para commandos, Navy SEALs, Air Force 
Garud, Marcos. Personnel strength: 15,000+ across all services. Training: 18+ months including international exposure. Specializations: 
hostage rescue, counter-terrorism, direct action raids, intelligence gathering. Equipment: advanced weapons, tactical gear, night vision, 
communication systems. Annual budget: ₹2,000 crores. Modernization: new aircraft platforms, advanced drone systems, cyber-integrated operations. 
Deployment: peacekeeping missions, counter-terrorism operations, strategic security."""
        },
        {
            "title": "Intelligence Collection and Analysis: Multi-Source Fusion System",
            "document_type": "Technical Document",
            "content": """Integrated intelligence collection and analysis system combining human intelligence, signals intelligence, 
imagery intelligence, and open-source intelligence. Collection assets: 200+ reconnaissance aircraft, 50+ surveillance satellites, 
HUMINT networks, SIGINT systems. Analysis centers: 15+ major intelligence fusion centers. Technology: AI-based pattern recognition, 
predictive analytics, automated threat detection. Processing capacity: 100+ terabytes daily. Personnel: 5,000+ trained intelligence analysts. 
Annual budget: ₹3,000 crores. Cooperation with allied intelligence agencies."""
        },
        {
            "title": "Electronic Warfare and Communications Security Framework",
            "document_type": "Technical Strategy",
            "content": """Comprehensive electronic warfare and communications security framework. Capabilities: radar jamming, signal interception 
and analysis, electronic counter-measures. Hardware: EW pods on aircraft, shipborne systems, ground-based stations. Software: advanced 
signal processing, AI-based threat classification, autonomous response systems. Communications security: encrypted networks, quantum key 
distribution, multi-layered encryption. Coordination: joint task forces, coordinated EW operations. Training: 2,000+ EW specialists annually. 
Budget: ₹5,000 crores over 5 years."""
        },
    ]
    documents.extend(special_docs)
    
    # ===== INFRASTRUCTURE & LOGISTICS DOCUMENTS =====
    infrastructure_docs = [
        {
            "title": "Defence Infrastructure Development: Strategic Bases and Facilities",
            "document_type": "Infrastructure Plan",
            "content": """Comprehensive defence infrastructure development plan for next 10 years. New strategic bases: 5 new air force bases, 
3 new naval bases, 2 new army cantonment areas. Expansion of existing facilities: 15 bases receiving modernization. Investment: ₹50,000 
crores over 10 years. Focus areas: forward deployment capabilities, coastal defence infrastructure, remote border area facilities. 
Technology integration: smart bases with IoT, automated systems, renewable energy. Accommodation: improving living standards for 500,000+ 
defence personnel. Estimated job creation: 100,000+ through construction and operations."""
        },
        {
            "title": "Logistics and Supply Chain Optimization: AI-Enabled Inventory Management",
            "document_type": "Operational System",
            "content": """AI-enabled logistics and supply chain management system for defence forces. Inventory management: real-time tracking, 
demand prediction, optimization algorithms. Distribution network: 500+ supply depots, automated routing, drone-based delivery in remote areas. 
Vendor management: 2,000+ approved suppliers, quality assurance, price negotiation. Spare parts management: critical spares inventory, 
predictive maintenance-based ordering. Cost reduction: 20-30% through optimization. Technology investment: ₹1,000 crores. Personnel training: 
5,000+ logistics personnel. Expected savings: ₹5,000 crores annually."""
        },
        {
            "title": "Medical and Healthcare Infrastructure for Defence Services",
            "document_type": "Healthcare Document",
            "content": """Comprehensive healthcare infrastructure for 2M+ defence personnel and families. Medical facilities: 50+ hospitals, 
200+ dispensaries, specialized trauma centers. Capability: trauma surgery, orthopaedics, cardiology, neurosurgery. Personnel: 10,000+ medical 
staff including 2,000+ doctors. Technology: telemedicine networks connecting remote bases, advanced diagnostic equipment, robotic surgery systems. 
Mental health services: counseling centers, stress management programs. Preventive care: fitness programs, health screening camps. 
Annual budget: ₹8,000 crores."""
        },
    ]
    documents.extend(infrastructure_docs)
    
    # ===== ENVIRONMENTAL & SUSTAINABILITY DOCUMENTS =====
    sustainability_docs = [
        {
            "title": "Green Defence Initiative: Renewable Energy and Environmental Sustainability",
            "document_type": "Sustainability Document",
            "content": """Defence forces sustainability initiative targeting carbon neutrality by 2050. Renewable energy: 500MW solar capacity 
by 2030, 100MW wind capacity, bio-fuel research. Energy efficiency: LED lighting conversion, building insulation, smart grid systems. 
Target: 50% renewable energy in operations by 2030. Water conservation: rainwater harvesting, recycled water usage, treatment systems. 
Waste management: 90% waste recycling target, hazardous waste disposal facilities. Environmental monitoring: wildlife protection, ecosystem 
preservation in strategic areas. Budget: ₹2,000 crores. Expected CO2 reduction: 40% by 2035."""
        },
        {
            "title": "Climate-Induced Security Challenges and Adaptation Strategies",
            "document_type": "Strategic Assessment",
            "content": """Assessment of climate-induced security challenges and military adaptation strategies. Identified risks: sea level rise 
threatening coastal installations, glacier melt affecting mountain warfare, extreme weather events, resource scarcity. Adaptation measures: 
base relocation planning, infrastructure hardening, water security systems. Operational adaptation: climate-aware training, equipment 
modifications for extreme conditions, supply chain resilience. Research initiatives: climate modeling for military planning, technology 
development for climate challenges. Budget allocation: ₹3,000 crores over 10 years. International cooperation: climate security forums, 
shared research initiatives."""
        },
    ]
    documents.extend(sustainability_docs)
    
    return documents

def save_documents_to_database():
    """Save generated documents to database"""
    
    print("\n" + "="*70)
    print("PHASE 4A: DOCUMENT COLLECTION AND INDEXING")
    print("="*70 + "\n")
    
    start_time = time.time()
    
    try:
        from src.shared.database import SessionLocal
        from src.models.document import Document, DocumentChunk
        from src.services.text_processor import get_text_processor
        
        db = SessionLocal()
        
        # Generate documents
        print("📚 Generating defence documents...")
        documents = generate_defence_documents()
        total_docs = len(documents)
        print(f"   ✓ Generated {total_docs} documents\n")
        
        # Save to database
        print(f"💾 Saving {total_docs} documents to database...")
        
        saved_count = 0
        duplicate_count = 0
        error_count = 0
        
        for idx, doc_data in enumerate(documents, 1):
            try:
                # Check for duplicates
                existing = db.query(Document).filter(
                    Document.title == doc_data['title']
                ).first()
                
                if existing:
                    duplicate_count += 1
                    print(f"   ⊘ [{idx:3d}] Duplicate: {doc_data['title'][:50]}")
                    continue
                
                # Create document
                doc = Document(
                    title=doc_data['title'],
                    content_raw=doc_data['content'],
                    content_processed=doc_data['content'],
                    document_type=doc_data['document_type'],
                    source_url=f"internal://document_{idx}",
                    status="ocr_complete",
                    ocr_confidence=0.95
                )
                
                db.add(doc)
                saved_count += 1
                
                # Print progress
                if idx % 10 == 0 or idx == total_docs:
                    print(f"   ✓ Saved {saved_count} documents...")
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error saving document {idx}: {str(e)}")
        
        db.commit()
        
        print(f"\n   ✓ Successfully saved {saved_count} documents")
        if duplicate_count > 0:
            print(f"   ⊘ Skipped {duplicate_count} duplicates")
        if error_count > 0:
            print(f"   ✗ Failed to save {error_count} documents")
        
        # Now chunk the new documents
        print(f"\n📑 Chunking all documents with semantic strategy...")
        
        text_processor = get_text_processor(chunk_size=512, chunk_overlap=100, strategy="semantic")
        new_docs = db.query(Document).filter(Document.id > 9).all()  # ID > 9 are the new ones
        
        total_chunks = 0
        for idx, doc in enumerate(new_docs, 1):
            try:
                # Delete old chunks if any
                db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).delete()
                
                # Re-chunk document
                chunks = text_processor.chunk_document(
                    doc.content_raw, 
                    document_id=doc.id,
                    db=db,
                    document_type=doc.document_type
                )
                
                if chunks:
                    for chunk_text, chunk_idx in chunks:
                        chunk_obj = DocumentChunk(
                            document_id=doc.id,
                            chunk_text=chunk_text,
                            chunk_index=chunk_idx,
                            token_count=len(chunk_text.split())
                        )
                        db.add(chunk_obj)
                        total_chunks += 1
                    
                    if idx % 5 == 0 or idx == len(new_docs):
                        print(f"   ✓ Chunked {idx}/{len(new_docs)} documents ({total_chunks} chunks total)...")
            except Exception as e:
                logger.error(f"Error chunking document {doc.id} ({doc.title}): {str(e)}")
        
        db.commit()
        print(f"   ✓ Created {total_chunks} chunks from {len(new_docs)} documents")
        
        # Now re-index with embeddings
        print(f"\n📑 Re-indexing all documents with embeddings...")
        
        from src.services.indexer import DocumentIndexer
        
        indexer = DocumentIndexer()
        result = indexer.index_all_documents(db, batch_size=32, skip_indexed=False)
        
        print(f"   ✓ Indexing status: {result['status']}")
        print(f"   ✓ Documents indexed: {result.get('total_documents', 0)}")
        print(f"   ✓ Total chunks indexed: {result.get('total_chunks', 0)}")
        print(f"   ✓ Duration: {result.get('duration_seconds', 0):.1f}s")
        
        if result.get('errors'):
            print(f"   ⚠ Indexing errors: {len(result['errors'])}")
        
        # Summary
        duration = time.time() - start_time
        
        print("\n" + "="*70)
        print("✅ PHASE 4A COLLECTION COMPLETE")
        print("="*70)
        print(f"Total time: {duration:.1f} seconds")
        print(f"\nResults:")
        print(f"  • Generated documents: {total_docs}")
        print(f"  • Saved documents: {saved_count}")
        print(f"  • Duplicates skipped: {duplicate_count}")
        print(f"  • Errors: {error_count}")
        print(f"  • Chunks created: {total_chunks}")
        print(f"  • Documents indexed: {result.get('total_documents', 0)}")
        print(f"  • Total in database: {9 + saved_count} (9 original + {saved_count} new)")
        print("="*70 + "\n")
        
        return {
            "status": "success",
            "duration": duration,
            "generated": total_docs,
            "saved": saved_count,
            "duplicates": duplicate_count,
            "errors": error_count,
            "chunks_created": total_chunks,
            "indexed_documents": result.get('total_documents', 0),
        }
        
    except Exception as e:
        logger.error(f"Collection failed: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "duration": time.time() - start_time
        }

if __name__ == "__main__":
    result = save_documents_to_database()
    sys.exit(0 if result["status"] == "success" else 1)
