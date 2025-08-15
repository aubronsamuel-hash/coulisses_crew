#!/usr/bin/env python3
"""Seed data for development/demo purposes."""
import argparse
import datetime as dt
import json
from pathlib import Path
import bcrypt

DATA_FILE = Path("data/data.json")


def _init_storage(reset: bool = False) -> dict:
    if reset and DATA_FILE.exists():
        DATA_FILE.unlink()
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w") as f:
            json.dump({"users": [], "missions": [], "assignments": []}, f)
    with DATA_FILE.open() as f:
        return json.load(f)


def _save_storage(data: dict) -> None:
    with DATA_FILE.open("w") as f:
        json.dump(data, f)


def seed_users(data: dict, count: int) -> None:
    users = data["users"]
    users.clear()
    # admin user
    pwd = bcrypt.hashpw(b"admin", bcrypt.gensalt()).decode()
    users.append({"id": 1, "username": "admin", "password_hash": pwd, "role": "admin"})
    uid = 2
    for i in range(count):
        pwd = bcrypt.hashpw(b"password", bcrypt.gensalt()).decode()
        users.append(
            {
                "id": uid,
                "username": f"user{i+1}",
                "password_hash": pwd,
                "role": "intermittent",
            }
        )
        uid += 1


def seed_missions(data: dict, count: int, days: int) -> None:
    missions = data["missions"]
    assignments = data["assignments"]
    missions.clear()
    assignments.clear()
    today = dt.date.today()
    mid = 1
    aid = 1
    user_ids = [u["id"] for u in data["users"] if u["role"] == "intermittent"]
    for i in range(count):
        day = today + dt.timedelta(days=i % max(days, 1))
        missions.append({"id": mid, "title": f"Mission {i+1}", "day": day.isoformat()})
        if user_ids:
            uid = user_ids[i % len(user_ids)]
            assignments.append({"id": aid, "mission_id": mid, "user_id": uid})
            aid += 1
        mid += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo data.")
    parser.add_argument(
        "--reset", action="store_true", help="Reset data file before seeding"
    )
    parser.add_argument(
        "--users", type=int, default=0, help="Number of intermittent users to create"
    )
    parser.add_argument(
        "--missions", type=int, default=0, help="Number of missions to create"
    )
    parser.add_argument(
        "--days", type=int, default=1, help="Spread missions over this many days"
    )
    parser.add_argument("--all", action="store_true", help="Seed everything")
    parser.add_argument(
        "--force-insert", action="store_true", help="Ignored, for compatibility"
    )
    args = parser.parse_args()

    data = _init_storage(reset=args.reset)
    if args.all:
        seed_users(data, args.users)
        seed_missions(data, args.missions, args.days)
    else:
        if args.users:
            seed_users(data, args.users)
        if args.missions:
            seed_missions(data, args.missions, args.days)
    _save_storage(data)


if __name__ == "__main__":
    main()
