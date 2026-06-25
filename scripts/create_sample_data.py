#!/usr/bin/env python
"""
Create sample documents and populate vector store for RAG pipeline testing
DIRAS Phase 4 - Sample Data Generation
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.shared.database import SessionLocal, init_db
from src.models.document import Document
from src.services.embeddings import get_embedding_generator
from src.services.vectorstore import get_vector_store
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sample government documents for testing RAG pipeline
SAMPLE_DOCUMENTS = [
    {
        "title": "Defence Procurement Policy 2023 - Strategic Framework",
        "source_url": "https://pib.gov.in/defence-procurement-policy-2023",
        "source_type": "PIB",
        "document_type": "Policy",
        "published_date": (datetime.now() - timedelta(days=180)).isoformat(),
        "content": """Defence Procurement Policy 2023 establishes comprehensive framework for acquisition of defence equipment.
        Key priorities: Make in India (50% indigenous content), Technology Transfer for strategic systems, FDI enhancement,
        Transparent e-bidding procurement, and Gestation support for MSMEs in defence. Procurement timeline: 18 months from RFP.
        Applies to Army, Navy, and Air Force with service-specific guidelines. All decisions documented for transparency."""
    },
    {
        "title": "Defence Budget Allocation 2023-24: Analysis",
        "source_url": "https://mod.gov.in/defence-budget-2023-24",
        "source_type": "MOD",
        "document_type": "Report",
        "published_date": (datetime.now() - timedelta(days=200)).isoformat(),
        "content": """Defence Budget 2023-24: ₹1.72 lakh crores (1.9% of GDP). Distribution: Capital 38% (₹65,000Cr),
        Revenue 62% (₹1,07,000Cr). Service allocation: Army 40%, Navy 20%, Air Force 25%, Strategic Forces 15%.
        Major projects: Project 75-I submarines (₹42,000Cr), FRCN aircraft (₹15,000Cr), Rafale production (₹8,000Cr),
        INS Vikrant (₹20,000Cr), Missile systems (₹12,000Cr). Supports 1.3 million defence personnel."""
    },
    {
        "title": "Military Modernization Strategy: 2023-2035",
        "source_url": "https://mod.gov.in/military-modernization-strategy",
        "source_type": "MOD",
        "document_type": "Strategic Document",
        "published_date": (datetime.now() - timedelta(days=150)).isoformat(),
        "content": """Military Modernization focuses on: Technology acquisition with indigenous development, 80% self-reliance by 2030,
        Joint operations capability, Advanced cybersecurity, and Military space applications. Priority areas: Hypersonic missiles,
        5G networks, Unmanned systems, AI integration, and Quantum computing research. Joint C4I systems for interoperability.
        Indigenous development of critical platforms with foreign collaboration for bleeding-edge technology."""
    },
    {
        "title": "Maritime Security Doctrine and Naval Strategy",
        "source_url": "https://indiannavy.nic.in/maritime-security-doctrine",
        "source_type": "Navy",
        "document_type": "Doctrine",
        "published_date": (datetime.now() - timedelta(days=120)).isoformat(),
        "content": """Indian Navy's Maritime Security Strategy emphasizes: Protection of maritime trade routes, 
        Counter-piracy operations, Submarine deterrence, Aircraft carrier operations, and Regional cooperation.
        Fleet composition: 2 operational carriers (INS Vikramaditya, INS Vikrant), 8+ major submarines, 24 frigates.
        Focus on Indo-Pacific presence, Quad cooperation, and Indian Ocean Region dominance. Ongoing modernization with
        indigenous platform development and advanced weaponry including cruise missiles and stealth frigates."""
    },
    {
        "title": "Cyber Warfare and Defence Cyber Strategy",
        "source_url": "https://mod.gov.in/cyber-warfare-strategy",
        "source_type": "MOD",
        "document_type": "Strategy Document",
        "published_date": (datetime.now() - timedelta(days=100)).isoformat(),
        "content": """Defence Cyber Strategy addresses: Critical infrastructure protection, Network security operations,
        Offensive cyber capabilities, Threat intelligence, and Rapid response mechanisms. Establishment of Cyber Command
        with 24/7 monitoring. Defense against state-sponsored cyber attacks and information warfare. Integration with
        NATO cyber defense frameworks. Focus on AI-based threat detection, machine learning for anomaly detection, and
        real-time security incident response protocols."""
    },
    {
        "title": "Unmanned Systems and Autonomous Weapons Development",
        "source_url": "https://mod.gov.in/unmanned-systems-policy",
        "source_type": "MOD",
        "document_type": "Policy",
        "published_date": (datetime.now() - timedelta(days=90)).isoformat(),
        "content": """Unmanned Systems Policy: Development of autonomous drones, UAVs, underwater drones, and autonomous vehicles.
        Programs: Rustom-II MALE UAV, Archer unmanned aerial target, Deep Sea Autonomous Vehicles, and Autonomous ground vehicles.
        Swarm drone technology development. Counter-drone systems and anti-UAV capabilities. Integration with AI for autonomous
        decision-making. Ethical guidelines for autonomous weapons. Focus on indigenous development with partnerships."""
    },
    {
        "title": "Nuclear Strategy and Strategic Forces Command",
        "source_url": "https://mod.gov.in/nuclear-doctrine",
        "source_type": "MOD",
        "document_type": "Doctrine",
        "published_date": (datetime.now() - timedelta(days=110)).isoformat(),
        "content": """India's Nuclear Doctrine based on: No first use, Credible second strike capability, Minimum deterrence.
        Strategic Forces Command manages: Agni missile series (I-VI), Submarines with ballistic missiles (INS Arihant class),
        and Air-based delivery systems. Triad-based deterrence with land, sea, and air-based platforms. Advanced early warning systems.
        Focus on survivability, redundancy, and secure command and control. No-first-use policy maintained for decades."""
    },
    {
        "title": "Defence Technology and Innovation Hub",
        "source_url": "https://mod.gov.in/defence-technology-hub",
        "source_type": "MOD",
        "document_type": "Initiative",
        "published_date": (datetime.now() - timedelta(days=80)).isoformat(),
        "content": """Defence Innovation Hub accelerates technology development through: Startup partnerships, Dual-use technology,
        Private sector collaboration, and Academia integration. Focus areas: Artificial intelligence, Machine learning, Big data,
        Quantum computing, and Biotechnology. iDEX (Innovation for Defence Excellence) program for startups. Technology transfer
        to defence PSUs. Incubation centers in major cities. Accelerated procurement for innovative technologies."""
    },
    {
        "title": "Air Defence Systems and Anti-Air Warfare",
        "source_url": "https://mod.gov.in/air-defence-systems",
        "source_type": "IAF",
        "document_type": "Technical Document",
        "published_date": (datetime.now() - timedelta(days=95)).isoformat(),
        "content": """Air Defence Capabilities: S-400 long-range systems (340 km range), Akash missiles (35 km range),
        Tunguska air-defence systems, and Advanced Radar networks. Fighter fleet: Tejas LCA, Rafale, Su-30MKI, Mirage-2000.
        Airborne Early Warning and Control systems (AEW&C). Network-centric warfare integration. Air traffic management systems.
        Future: 5G-enabled air defence network, Hypersonic threat detection, and AI-powered command and control systems."""
    },
    {
        "title": "Land Combat Modernization and Infantry Systems",
        "source_url": "https://mod.gov.in/land-combat-modernization",
        "source_type": "Army",
        "document_type": "Modernization Plan",
        "published_date": (datetime.now() - timedelta(days=85)).isoformat(),
        "content": """Land Combat Modernization: Main Battle Tanks (Arjun, T-72M1), Infantry Combat Vehicles (BMP-2, Stryker variants),
        Artillery systems (Bofors guns, Advanced towed artillery). Soldier modernization with digital systems, body armor, and
        night-vision equipment. Network-centric warfare for battalion-level operations. Loitering munitions (Kamikaze drones).
        Future platforms: Autonomous ground vehicles, Exoskeleton systems, and AI-powered command systems."""
    },
    {
        "title": "Defence Industry Standards and Quality Assurance",
        "source_url": "https://mod.gov.in/defence-standards",
        "source_type": "MOD",
        "document_type": "Standards",
        "published_date": (datetime.now() - timedelta(days=75)).isoformat(),
        "content": """Defence Standards and Quality: ISO certification requirements for defence manufacturers. BIS/ISI marks for critical
        components. Third-party inspection protocols. Environmental compliance for defence manufacturing. Safety standards for
        weapons systems. Reliability and durability testing for equipment. Supply chain transparency and vendor management."""
    }
]

def create_sample_documents():
    """Create and populate sample documents in database and vector store"""
    
    logger.info("=" * 80)
    logger.info("DIRAS Sample Data Generator - Phase 4")
    logger.info("=" * 80)
    
    try:
        # Initialize database
        logger.info("\n1. Initializing database...")
        init_db()
        session = SessionLocal()
        logger.info("   ✓ Database initialized")
        
        # Get embeddings and vector store
        logger.info("\n2. Loading embedding model and vector store...")
        embeddings_svc = get_embedding_generator()
        vector_store = get_vector_store()
        logger.info("   ✓ Embedding model loaded")
        logger.info("   ✓ Vector store ready")
        
        # Create documents
        logger.info(f"\n3. Creating {len(SAMPLE_DOCUMENTS)} sample documents...")
        created_count = 0
        
        for doc_data in SAMPLE_DOCUMENTS:
            # Create database record
            doc = Document(
                title=doc_data["title"],
                content_raw=doc_data["content"],
                content_processed=doc_data["content"],
                source_url=doc_data["source_url"],
                source_type=doc_data["source_type"],
                document_type=doc_data["document_type"],
                published_date=datetime.fromisoformat(doc_data["published_date"]),
                is_indexed=True
            )
            session.add(doc)
            session.flush()  # Get the ID
            
            # Generate embeddings and add to vector store
            embedding = embeddings_svc.embed_text(doc_data["content"])
            vector_store.add_document(
                doc_id=str(doc.id),
                content=doc_data["content"],
                embedding=embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
                metadata={
                    "title": doc.title,
                    "source": doc.source_url,
                    "type": doc.document_type,
                    "date": doc.published_date.isoformat()
                }
            )
            
            created_count += 1
            logger.info(f"   ✓ [{created_count}/{len(SAMPLE_DOCUMENTS)}] {doc.title[:60]}...")
        
        session.commit()
        logger.info(f"\n✓ Successfully created {created_count} documents")
        
        # Display sample test queries
        logger.info("\n" + "=" * 80)
        logger.info("SAMPLE TEST QUERIES FOR RAG PIPELINE:")
        logger.info("=" * 80)
        
        test_queries = [
            "What is the Defence Procurement Policy 2023?",
            "What is the defence budget allocation for 2023-24?",
            "Tell me about military modernization strategy",
            "What are India's maritime security capabilities?",
            "Explain the nuclear doctrine and strategic forces",
            "What cyber warfare strategies does India have?",
            "Describe unmanned systems development in India",
            "What air defence systems are available?",
        ]
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"\n{i}. {query}")
        
        logger.info("\n" + "=" * 80)
        logger.info("START THE BACKEND:")
        logger.info("  uvicorn src.api.main:app --host 0.0.0.0 --port 8000")
        logger.info("\nTEST WITH CURL:")
        logger.info('  curl -X POST "http://localhost:8000/api/v1/query"')
        logger.info('       -H "Content-Type: application/json"')
        logger.info('       -d \'{"question":"What is Defence Procurement Policy?"}\' ')
        logger.info("=" * 80)
        
        session.close()
        logger.info("\n✓ Sample data generation complete!")
        return True
        
    except Exception as e:
        logger.error(f"\n✗ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_sample_documents()
    sys.exit(0 if success else 1)
