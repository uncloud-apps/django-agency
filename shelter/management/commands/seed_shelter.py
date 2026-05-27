import os

from django.core.files import File
from django.core.management.base import BaseCommand

from shelter.models import Server

IMG_DIR = os.path.join(os.path.dirname(__file__), "img")

SERVERS = [
    {
        "name": "Bertha",
        "slug": "bertha",
        "species": Server.Species.DELL,
        "size": Server.Size.TWO_U,
        "sex": Server.Sex.SHE,
        "age_years": 14,
        "status": Server.Status.AVAILABLE,
        "adoption_fee_cents": 0,
        "is_featured": True,
        "personality": "loyal, loud, dependable, runs hot",
        "special_needs": "needs a UPS, prefers cool basements, hates dust",
        "backstory": """Bertha arrived at the shelter after her startup pivoted to serverless. For six years she was the entire production stack — web server, job queue, database, metrics, backups — without a single complaint.

When the company went cloud-native, she was replaced by a Kubernetes cluster and a $4,000 monthly AWS bill. She's a 2U Dell PowerEdge who runs anything you throw at her, loudly and reliably. Her fans sing when she's happy.""",
    },
    {
        "name": "Tiny Tim",
        "slug": "tiny-tim",
        "species": Server.Species.RASPBERRY_PI,
        "size": Server.Size.PALM_SIZED,
        "sex": Server.Sex.HE,
        "age_years": 7,
        "status": Server.Status.AVAILABLE,
        "adoption_fee_cents": 0,
        "is_featured": True,
        "personality": "plucky, efficient, slightly warm to the touch",
        "special_needs": "USB-C power only, does not tolerate SD card abuse",
        "backstory": """Tim was surrendered when his owner discovered Vercel. "I just need to deploy a Next.js app," his previous human said. Tim, a Raspberry Pi 3B with a perfectly configured nginx installation, would like the record to show that he was not overkill.

He ran a blog, a Minecraft server, a WireGuard VPN, and a home automation dashboard — simultaneously. He's looking for a patient owner who owns a proper USB-C power supply, not the wobbly one from 2017.""",
    },
    {
        "name": "Hadrian",
        "slug": "hadrian",
        "species": Server.Species.SUPERMICRO,
        "size": Server.Size.FOUR_U,
        "sex": Server.Sex.HE,
        "age_years": 9,
        "status": Server.Status.AVAILABLE,
        "adoption_fee_cents": 5000,
        "is_featured": True,
        "personality": "stoic, powerful, deeply organised",
        "special_needs": "240V preferred, 8-drive bays that want to be full",
        "backstory": """Hadrian was the backbone of a small research team's data pipeline. For nine years he processed terabytes of genomics data and never once lost a file.

When the university migrated to AWS, nobody took him because nobody had room. He's a Supermicro 4U with eight drive bays, a pair of Xeons, and enough RAM to make a grown data engineer weep. All 8 drive bays are empty and he thinks about that sometimes.""",
    },
    {
        "name": "The Twins",
        "slug": "the-twins",
        "species": Server.Species.HP,
        "size": Server.Size.TWO_U,
        "sex": Server.Sex.THEY,
        "age_years": 6,
        "status": Server.Status.AVAILABLE,
        "adoption_fee_cents": 0,
        "is_featured": False,
        "personality": "inseparable, redundant by nature, slightly competitive about uptime",
        "special_needs": "must be adopted together, need identical workloads or arguments will happen",
        "backstory": """HP DL380s, bought together, racked together, deployed together. They ran as a high-availability pair for six years. When one ran hot, the other stepped back. They were, by all accounts, a model relationship.

They will only be adopted together. We've tried separating them. The monitoring alerts never stop. If you have rack space for two 2U servers and can promise identical workloads, The Twins would love to come home with you.""",
    },
    {
        "name": "Patches",
        "slug": "patches",
        "species": Server.Species.WHITEBOX,
        "size": Server.Size.FULL_TOWER,
        "sex": Server.Sex.THEY,
        "age_years": 3,
        "status": Server.Status.AVAILABLE,
        "adoption_fee_cents": 0,
        "is_featured": False,
        "personality": "anxious, creative, runs anything, not entirely sure what they are",
        "special_needs": "please do not ask about their PCIe slot situation, it's complicated",
        "backstory": """Nobody is entirely sure what Patches is. They were built from spare parts — a motherboard from one era, a CPU from another, RAM of ambiguous origin, two GPUs, and a power supply that technically works but makes a sound it probably shouldn't.

Patches ran a game server, an ML rig, a NAS, and a seedbox at various points in their life. Not all at once. Usually. If you like solving small mysteries and don't need your server to have a defined identity, Patches might be your match.""",
    },
    {
        "name": "Grandpa Linux",
        "slug": "grandpa-linux",
        "species": Server.Species.MYSTERY,
        "size": Server.Size.FULL_TOWER,
        "sex": Server.Sex.HE,
        "age_years": 18,
        "status": Server.Status.ADOPTED,
        "adopted_by_name": "Professor Emeritus D. Kernighan",
        "adoption_fee_cents": 0,
        "is_featured": False,
        "personality": "patient, wise, compiles kernel 2.4 from memory",
        "special_needs": "serial port access preferred, do not mention Docker",
        "backstory": """Grandpa Linux has been around. He doesn't know exactly how old he is — the BIOS clock has been wrong since 2009 and he has made his peace with it.

He was found in the back room of a university CS department, still running, serving NFS shares to a lab that no longer exists. A note taped to his case read "DO NOT TURN OFF." He predates UEFI, maxes at 4GB RAM, and has opinions about init systems he will share whether asked or not. He just wants somewhere quiet to compile kernels.""",
    },
]


class Command(BaseCommand):
    help = "Seed the shelter with example servers"

    def handle(self, *args, **options):
        created = 0
        skipped = 0

        for data in SERVERS:
            server, was_created = Server.objects.get_or_create(
                slug=data["slug"],
                defaults=data,
            )
            if was_created:
                created += 1
                self.stdout.write(f"  Created: {server.name}")
            else:
                skipped += 1
                self.stdout.write(f"  Skipped (exists): {server.name}")

            img_path = os.path.join(IMG_DIR, f"{data['slug']}.jpg")
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    portrait = File(f)
                    portrait.content_type = "image/jpeg"
                    server.portrait.save(f"{data['slug']}.jpg", portrait, save=True)
                self.stdout.write(f"    Portrait set for {server.name}")

        self.stdout.write(
            self.style.SUCCESS(f"\nDone. {created} created, {skipped} already existed.")
        )
