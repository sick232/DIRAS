#!/usr/bin/env python
"""
Seed DIRAS database with sample government documents for testing
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.shared.database import SessionLocal, init_db
from src.models.document import Document, DocumentChunk, Embedding
from src.services.text_processor import get_text_processor
from src.services.embeddings import get_embedding_generator
from src.services.vectorstore import get_vector_store
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample government documents for testing
SAMPLE_DOCUMENTS = [
    {
        "title": "Defence Procurement Policy 2023 - Strategic Framework",
        "source_url": "https://pib.gov.in/defence-procurement-policy-2023",
        "source_type": "PIB",
        "document_type": "Policy",
        "published_date": datetime.now() - timedelta(days=180),
        "content": """
        The Defence Procurement Policy 2023 establishes a comprehensive framework for acquisition of defence equipment 
        and systems. The policy emphasizes indigenous development, self-reliance, and technology transfer. Key priorities include:
        
        1. Make in India Initiative: Priority given to domestically manufactured defence systems with at least 50% indigenous content.
        2. Technology Transfer: Foreign vendors must commit to technology transfer agreements for strategic systems.
        3. FDI Enhancement: 100% FDI allowed in defence manufacturing with government approval for critical systems.
        4. Transparent Procurement: e-bidding systems and real-time tracking of all defence contracts.
        5. Gestation Support: Interest-free loans for MSMEs in defence manufacturing for first 5 years.
        
        The procurement process involves: Request for Proposal (RFP), Technical Evaluation, Financial Bid Opening, 
        Contract Negotiation, and Implementation with quarterly reviews. All decisions are documented for transparency.
        Defence procurement now follows a 18-month timeline from RFP to contract award to accelerate capability development.
        The policy applies to all three services: Army, Navy, and Air Force, with service-specific guidelines for their unique requirements.
        """
    },
    {
        "title": "Defence Budget Allocation 2023-24: Analysis and Distribution",
        "source_url": "https://mod.gov.in/defence-budget-2023-24",
        "source_type": "MOD",
        "document_type": "Report",
        "published_date": datetime.now() - timedelta(days=200),
        "content": """
        The Defence Budget for 2023-24 has been allocated ₹1.72 lakh crores, representing 1.9% of GDP. 
        This allocation reflects the government's commitment to modernization and operational readiness.
        
        Budget Distribution:
        - Capital Expenditure: ₹65,000 crores (38%) - New equipment, infrastructure, modernization
        - Revenue Expenditure: ₹1,07,000 crores (62%) - Salaries, operations, maintenance
        
        Key Allocations:
        - Army: ₹68,000 crores (40%) - Personnel, weapons, training
        - Navy: ₹35,000 crores (20%) - Maritime systems, submarines, aircraft carriers
        - Air Force: ₹44,000 crores (25%) - Fighter jets, transport aircraft, air defense
        - Strategic Forces: ₹25,000 crores (15%) - Nuclear deterrence, strategic systems
        
        Major Projects Funded:
        - Project 75-I: 6 Advanced Submarines (₹42,000 crores over 15 years)
        - FRCN: Fifth Generation Combat Aircraft (₹15,000 crores)
        - Rafale Production Line: 36 additional aircraft (₹8,000 crores)
        - Indigenous Aircraft Carrier (INS Vikrant): ₹20,000 crores
        - Missile Systems: BrahMos, Akash, QRSAM development (₹12,000 crores)
        
        The budget supports approximately 1.3 million military and civilian personnel in the defence sector.
        """
    },
    {
        "title": "Military Modernization Strategy: 2023-2035 Road Map",
        "source_url": "https://mod.gov.in/military-modernization-strategy",
        "source_type": "MOD",
        "document_type": "Strategic Document",
        "published_date": datetime.now() - timedelta(days=150),
        "content": """
        India's Military Modernization Strategy aims to create a technologically advanced, self-reliant defence force 
        capable of addressing emerging security challenges in the Indo-Pacific region.
        
        Strategic Pillars:
        1. Technology Acquisition: Import of cutting-edge platforms with simultaneous indigenous development
        2. Self-Reliance: 80% indigenous content in all new systems by 2030
        3. Joint Operations: Enhanced interoperability between services through common C4I systems
        4. Cybersecurity: Advanced cyber warfare capabilities and critical infrastructure protection
        5. Space Applications: Military satellites for surveillance, navigation, and communication
        
        Priority Areas:
        - Hypersonic Missiles: Mach 5+ cruise missiles under development
        - 5G Networks: Military-grade 5G for unmanned systems and battlefield communication
        - AI Integration: Autonomous systems for surveillance and decision support
        - Quantum Computing: Encryption and cryptographic applications for secure communication
        - Artificial Intelligence: Machine learning for target identification and predictive maintenance
        
        Partnerships:
        - Technology partnerships with USA, France, Israel, Russia, and Japan
        - Co-development arrangements for systems like fighter jets and helicopters
        - Joint exercises and interoperability protocols with friendly nations
        
        Timeline: Capability goals set for 2025, 2028, 2032, and 2035 with measurable metrics.
        """
    },
    {
        "title": "Cybersecurity Strategy for Defence Installations 2023",
        "source_url": "https://dod.gov.in/cybersecurity-defence-2023",
        "source_type": "MOD",
        "document_type": "Security Policy",
        "published_date": datetime.now() - timedelta(days=120),
        "content": """
        The Defence Cybersecurity Strategy outlines measures to protect critical military infrastructure, communication networks, 
        and information systems from cyber threats, both state-sponsored and non-state actors.
        
        Threat Assessment:
        - Nation-state adversaries targeting defence secrets and military capabilities
        - Espionage activities targeting classified information and strategic plans
        - Disruption attempts against operational command and control systems
        - Theft of defense technology and intellectual property
        
        Defensive Measures:
        - Zero Trust Architecture: All access requires verification, no implicit trust
        - End-to-End Encryption: All sensitive communications use military-grade encryption (AES-256)
        - Multi-Factor Authentication: All personnel use biometric + password + hardware tokens
        - Air-Gapped Networks: Critical systems isolated from internet connectivity
        - Continuous Monitoring: 24/7 intrusion detection and prevention systems
        
        Operational Protocols:
        - Defense Information Systems Agency (DISA) standards for network design
        - Regular penetration testing by authorized ethical hackers (quarterly)
        - Security incident response within 4 hours of detection
        - Personnel security clearances updated annually with background verification
        - Equipment procurement from certified vendors with security audits
        
        Incident Response:
        - Cyber Incident Response Team (CIRT) activated within 15 minutes of threat detection
        - Forensics preserved for investigation and prosecution
        - Affected systems isolated within 30 minutes to prevent spread
        """
    },
    {
        "title": "Advanced Weaponry Systems: Development and Deployment",
        "source_url": "https://mod.gov.in/weapons-systems-2023",
        "source_type": "MOD",
        "document_type": "Technical Report",
        "published_date": datetime.now() - timedelta(days=100),
        "content": """
        This report details India's advanced weaponry systems currently in development or recently deployed, 
        showcasing indigenous technological capabilities and international partnerships.
        
        Missile Systems:
        - BrahMos Cruise Missile: Hypersonic (Mach 3+), range 450 km, sea and land variants operational
        - Akash-NG Air Defence System: Multi-target engagement, range 30 km, fully indigenous
        - QRSAM: Quick Reaction Surface-to-Air Missile, range 25 km, autonomous operation
        - PSLV/GSLV: Satellite launch systems with dual military applications
        - Nirbhay: Subsonic cruise missile under development for extended range operations
        
        Aircraft Systems:
        - Rafale Fighter Jet: 36 aircraft on order from France, integration with indigenous systems
        - Tejas Light Combat Aircraft: 83 aircraft approved, 10 operational, with continuous upgrades
        - HAL Prachand: Indigenous light combat helicopter, 15 in operation
        - Transport Aircraft: C-17 Globemaster, C-130J Hercules, ALH utility helicopters
        
        Naval Platforms:
        - INS Vikramaditya: Carrier with integrated air defense and communications systems
        - Project 75-I Submarines: Advanced diesel-electric submarines with AIP (Air Independent Propulsion)
        - Guided Missile Destroyers: INS Kolkata-class, equipped with Brahmos missiles
        - Corvettes and Offshore Patrol Vessels: Coastal security and territorial waters protection
        
        Ground Systems:
        - T-72 Tank Upgrades: Enhanced armor, fire control, and engine systems
        - Arjun Main Battle Tank: Indigenous design, 118 tanks in operation
        - Combat Management Systems: Integrated battlefield network and decision support
        """
    },
    {
        "title": "Indo-Pacific Security and Regional Defence Cooperation",
        "source_url": "https://mod.gov.in/indo-pacific-security-2023",
        "source_type": "MOD",
        "document_type": "Strategic Assessment",
        "published_date": datetime.now() - timedelta(days=90),
        "content": """
        India plays a crucial role in maintaining stability and security in the Indo-Pacific region, a geographically vast 
        area with significant maritime trade routes and strategic importance.
        
        Regional Challenges:
        - Maritime disputes in South China Sea and Indian Ocean
        - Terrorism and extremism affecting coastal security
        - Piracy and armed robbery in key shipping lanes
        - Unregulated arms trafficking and human trafficking
        - Climate change impacts on island nations and maritime zones
        
        Defence Partnerships:
        - Quad Alliance: USA, Japan, Australia, India cooperation for peace and stability
        - BIMSTEC: Bay of Bengal Initiative for regional security cooperation
        - ASEAN Engagement: Strategic dialogue and military cooperation exercises
        - Indian Ocean Rim Association: Coordination for maritime security
        
        Operational Activities:
        - Regular naval exercises: Malabar (USA, Japan, India), MILAN (regional navies)
        - Joint air exercises with friendly nations to build interoperability
        - Anti-piracy operations in Gulf of Aden and Indian Ocean
        - Disaster relief and humanitarian assistance missions
        
        Technology and Intelligence Sharing:
        - Real-time information sharing on maritime threats and piracy
        - Joint surveillance operations in critical sea lanes
        - Coordinated response to emerging security threats
        - Exchange of intelligence on terrorism and extremism funding
        
        Future Strategy:
        - Strengthening missile defense capabilities for regional credibility
        - Expanding naval presence with additional carrier battle groups
        - Building indigenous space-based surveillance and early warning systems
        - Enhanced cyber defense for critical maritime and port infrastructure
        """
    },
    {
        "title": "Personnel Training and Professional Development in Armed Forces",
        "source_url": "https://mod.gov.in/personnel-training-development",
        "source_type": "MOD",
        "document_type": "Policy Document",
        "published_date": datetime.now() - timedelta(days=75),
        "content": """
        The Armed Forces training and development program ensures that military personnel are equipped with 
        cutting-edge knowledge and skills for modern warfare.
        
        Officer Training Academies:
        - National Defence Academy (NDA): 4-year training for commission as officer
        - Officers Training Academy (OTA): 49-week training for graduate officers
        - Army Staff College: Senior officer strategy and leadership development
        - War Colleges: Highest level strategic and operational training
        
        Enlisted Personnel Training:
        - Basic Military Training Centers: 6-12 week initial training
        - Trade-specific Training: Pilots, engineers, medical, signals, etc.
        - Leadership Schools: NCO (Non-Commissioned Officer) advancement programs
        - Continuing Education: Annual refresher courses on latest tactics and technology
        
        Technology Training:
        - Pilot Training on Rafale, Tejas, and other aircraft
        - Submarine Crew Training: Advanced underwater warfare tactics
        - Cyber Warfare Training: Defense against digital threats
        - Artificial Intelligence Applications: Machine learning and autonomous systems
        - Unmanned Systems: Drone and robot operation and maintenance
        
        International Exchange:
        - Training exchanges with allied nations (USA, UK, France, Israel)
        - Joint exercises providing real-world training scenarios
        - Instructor attachments at foreign military academies
        - Participation in international military competitions
        
        Standards and Evaluation:
        - Rigorous evaluation standards ensuring combat readiness
        - Competency-based assessment of all critical skills
        - Regular audits of training effectiveness
        - Feedback loops for continuous improvement of curriculum
        """
    },
    {
        "title": "Defence Research and Development: Innovation in Military Technology",
        "source_url": "https://drdo.gov.in/research-development-2023",
        "source_type": "MOD",
        "document_type": "Research Report",
        "published_date": datetime.now() - timedelta(days=60),
        "content": """
        The Defence Research and Development Organisation (DRDO) is the premier R&D institution driving 
        technological self-reliance and innovation in defence systems.
        
        Research Laboratories:
        - Aeronautical Development Establishment (ADE): Aircraft and missile design
        - Defence Electronics Research Laboratory (DERL): Electronics and communications
        - Mechanical Engineering Research Laboratory (MERL): Ground systems and vehicles
        - Naval Science and Technological Laboratory (NSTL): Submarine and ship technology
        - Centre for Airborne Systems (CARS): Avionics and mission systems
        
        Major Projects:
        - FRCN: Fifth Generation Combat Aircraft (stealth, AI-enabled)
        - ASTRA Missile: Air-to-air missile with indigenous seekers and propulsion
        - Lakshya Target: Unmanned aerial vehicle for training and reconnaissance
        - Tactical Ballistic Missile (TBM): Short-range precision strike system
        
        Advanced Technologies:
        - Directed Energy Weapons: High-power laser and microwave systems
        - Quantum Radar: Detection system using quantum entanglement properties
        - Additive Manufacturing: 3D printing for complex defense components
        - Artificial Intelligence: Machine learning for autonomous systems
        - Biotechnology: Biological sensors and health monitoring systems
        
        Collaboration:
        - Industry partnerships with private sector for rapid development
        - Academic collaborations with universities for research
        - International partnerships with friendly nations for technology exchange
        - Startup ecosystem fostering innovation in defense tech startups
        
        Patents and Intellectual Property:
        - Over 400 patents filed in last 5 years in critical defense technologies
        - Technology transfer to private industry for commercial applications
        - Open innovation platforms for crowd-sourced problem solving
        """
    },
    {
        "title": "Veterans' Rehabilitation and Post-Service Support Program",
        "source_url": "https://mod.gov.in/veterans-rehabilitation-2023",
        "source_type": "MOD",
        "document_type": "Social Policy",
        "published_date": datetime.now() - timedelta(days=45),
        "content": """
        The Veterans' Rehabilitation and Post-Service Support Program ensures dignified rehabilitation 
        and reintegration of retired military personnel into civilian society.
        
        Healthcare Services:
        - Free medical treatment for service-connected disabilities at defense hospitals
        - ECHS (Ex-Servicemen Contribution Health Scheme): Pan-India medical network coverage
        - Mental health support and PTSD counseling for combat trauma
        - Geriatric care centers for aging veterans and their dependents
        - Artificial limbs and prosthetics for disabled veterans
        
        Financial Support:
        - Disability pensions based on extent of disability (0-100%)
        - Pension reviews every 3 years with inflation adjustments
        - One-time rehabilitation grant for economically backward veterans
        - Interest-free loans for business startup and self-employment
        - Housing assistance and concessional housing schemes
        
        Employment Assistance:
        - Priority employment in civilian government and PSU jobs
        - Skill development courses in high-demand sectors
        - Self-employment training and business mentoring
        - Job placement assistance through employment fairs
        - Reservation in police forces and paramilitary organizations
        
        Education Support:
        - Scholarship programs for children of war casualties
        - Concessional admission to defense institutes and universities
        - Vocational training in engineering and trades
        - Adult literacy programs for less educated veterans
        
        Community Integration:
        - Veteran peer support groups and networking organizations
        - Recreational facilities and sports programs
        - Cultural programs and ceremonial recognition events
        - Grievance redressal mechanism for benefits disputes
        """
    }
]


def seed_database():
    """Seed database with sample documents"""
    
    logger.info("\n" + "="*70)
    logger.info("SEEDING DIRAS DATABASE WITH SAMPLE DOCUMENTS")
    logger.info("="*70 + "\n")
    
    try:
        # Initialize database
        logger.info("📦 Initializing database...")
        init_db()
        logger.info("✓ Database initialized\n")
        
        # Get session
        db = SessionLocal()
        
        # Insert documents
        logger.info(f"📄 Inserting {len(SAMPLE_DOCUMENTS)} sample documents...")
        documents = []
        for i, doc_data in enumerate(SAMPLE_DOCUMENTS, 1):
            doc = Document(
                title=doc_data['title'],
                source_url=doc_data['source_url'],
                source_type=doc_data['source_type'],
                document_type=doc_data['document_type'],
                content_raw=doc_data['content'],
                content_processed=doc_data['content'],  # Already processed
                published_date=doc_data['published_date'],
                downloaded_date=datetime.utcnow(),
                status='ocr_complete',  # Mark as already processed
                ocr_confidence=0.95,
                is_indexed=False,
                doc_metadata={'source': 'seed_data', 'test': True}
            )
            db.add(doc)
            db.flush()  # Get ID
            documents.append(doc)
            logger.info(f"  [{i}/{len(SAMPLE_DOCUMENTS)}] {doc.title[:50]}...")
        
        db.commit()
        logger.info(f"✓ {len(documents)} documents inserted\n")
        
        # Process into chunks
        logger.info("✂️  Chunking documents...")
        text_processor = get_text_processor()
        chunk_count = 0
        
        for i, doc in enumerate(documents, 1):
            chunks_data = text_processor.chunk_document(
                doc.content_processed,
                document_id=doc.id,
                db=db
            )
            chunk_count += len(chunks_data)
            logger.info(f"  [{i}/{len(documents)}] Created {len(chunks_data)} chunks for {doc.title[:40]}...")
        
        db.commit()
        logger.info(f"✓ {chunk_count} chunks created\n")
        
        # Generate embeddings
        logger.info("🧠 Generating embeddings...")
        embedder = get_embedding_generator()
        
        # Get all unindexed chunks
        unindexed_chunks = db.query(DocumentChunk).filter(
            DocumentChunk.is_indexed == False
        ).all()
        
        logger.info(f"  Processing {len(unindexed_chunks)} chunks...")
        chunk_texts = [chunk.chunk_text for chunk in unindexed_chunks]
        
        # Embed in batches
        embeddings = embedder.embed_batch(chunk_texts, batch_size=32, show_progress=True)
        
        # Store embeddings
        for chunk, embedding_vector in zip(unindexed_chunks, embeddings):
            # Convert tensor to list if needed
            if hasattr(embedding_vector, 'tolist'):
                vector_list = embedding_vector.tolist()
            else:
                vector_list = list(embedding_vector) if isinstance(embedding_vector, (list, tuple)) else embedding_vector
            
            embedding = Embedding(
                chunk_id=chunk.id,
                vector=vector_list,
                model_name='all-MiniLM-L6-v2'
            )
            db.add(embedding)
            chunk.is_indexed = True
            db.add(chunk)
        
        db.commit()
        logger.info(f"✓ {len(embeddings)} embeddings created\n")
        
        # Index to ChromaDB
        logger.info("🔍 Indexing to ChromaDB...")
        vectorstore = get_vector_store()
        
        chunk_ids = [str(chunk.id) for chunk in unindexed_chunks]
        embedding_vectors = embeddings
        chunk_texts_list = chunk_texts
        
        # Prepare metadatas
        metadatas = []
        for chunk in unindexed_chunks:
            doc = db.query(Document).filter(Document.id == chunk.document_id).first()
            if doc:
                metadatas.append({
                    'document_id': doc.id,
                    'document_title': doc.title,
                    'chunk_index': chunk.chunk_index,
                    'source_url': doc.source_url,
                    'document_type': doc.document_type,
                    'source_type': doc.source_type
                })
        
        # Add to ChromaDB
        vectorstore.add_embeddings(
            chunk_ids=chunk_ids,
            embeddings=embedding_vectors,
            documents=chunk_texts_list,
            metadatas=metadatas
        )
        logger.info(f"✓ {len(chunk_ids)} embeddings indexed to ChromaDB\n")
        
        # Mark documents as indexed
        for doc in documents:
            doc.is_indexed = True
        db.commit()
        
        # Summary
        logger.info("="*70)
        logger.info("✅ SEEDING COMPLETE!")
        logger.info("="*70)
        logger.info(f"  📄 Documents: {len(documents)}")
        logger.info(f"  ✂️  Chunks: {chunk_count}")
        logger.info(f"  🧠 Embeddings: {len(embeddings)}")
        logger.info(f"  🔍 Indexed: {len(chunk_ids)} vectors in ChromaDB\n")
        
        logger.info("Next: Test queries with /api/v1/query endpoint")
        logger.info(f"Example: GET http://127.0.0.1:8001/api/v1/documents")
        logger.info(f"Example: GET http://127.0.0.1:8001/api/v1/index-status")
        logger.info(f"Example: POST http://127.0.0.1:8001/api/v1/query")
        logger.info("="*70 + "\n")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = seed_database()
    sys.exit(0 if success else 1)
