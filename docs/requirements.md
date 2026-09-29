# Synthetic salon pilot

Status: pilot acceptance contract. No customer data.

The first code task implements `can_book(existing, start, end)` in `salon_booking.py`.
Times are integer minutes. Existing bookings use half-open intervals.

- Accept a booking when its interval is positive and does not overlap.
- Reject overlapping bookings, including exact duplicates.
- Allow a booking ending when another begins.
- Reject zero-length and reversed intervals.

This narrow case tests the independent repository gate. It is not a complete salon product.
