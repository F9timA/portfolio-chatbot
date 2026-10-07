# Case Study: Safar — Bus Ticket Booking App

*(Draft — Fatima to review and refine details)*

## Role
Fatima led both the UI/UX design and the frontend development of Safar. She designed the complete user experience in Figma, then built it herself in Flutter with Firebase as the backend — making this one of her few projects that spans design through to a working, functional build rather than design alone.

## What It Does
Safar is a mobile bus ticket booking app aimed at simplifying a process that is often clunky and confusing on existing booking platforms. Users can search routes, view available buses, select seats from a visual seat map, apply filters (such as time, price, or bus type), and complete a booking — all through a clean, modern mobile interface.

## The Problem
Many existing bus booking apps and websites suffer from cluttered layouts, unclear seat availability, and confusing multi-step booking flows that cause user drop-off. Fatima designed Safar to solve this directly: a simplified, visual seat-selection experience, clear filtering so users can narrow down options quickly, and a streamlined booking flow with minimal steps between search and confirmation.

## Tech Stack
- **Flutter** — cross-platform mobile app framework used for development
- **Firebase** — backend services, including:
  - Authentication (user sign-up/login)
  - Real-time database features (for live seat availability and booking updates)
  - Data storage for routes, schedules, and bookings

## Key Design & Development Decisions

**Visual seat selection over list-based booking.** Rather than presenting seats as a plain list, Fatima designed an interactive seat-map interface so users can see exactly which seats are available, taken, or selected at a glance — closer to how people intuitively think about choosing a physical seat.

**Real-time data with Firebase.** Using Firebase's real-time capabilities meant seat availability could update live, reducing the risk of double-bookings and giving users confidence that what they see reflects the current state of the bus.

**Filtering built in from the start.** Filters for time, price, and bus type were designed as a core part of the search flow rather than an afterthought, since narrowing down options quickly was identified as a key usability need.

## Challenges
As both designer and developer on this project, Fatima had to translate her own high-fidelity Figma designs into working Flutter UI — a process that surfaced real constraints (spacing, component behavior, state management for the seat map) that pure design work doesn't expose. This gave her a much closer feedback loop between design intent and implementation reality than design-only projects allow.

## Why This Project Matters
Safar shows Fatima's ability to take a project from concept through visual design to a working, integrated product — not just static UI screens. It demonstrates end-to-end product thinking: identifying a real user pain point (messy booking flows), designing a targeted solution (visual seat selection, built-in filtering), and implementing it with a real backend (Firebase authentication and real-time data).
