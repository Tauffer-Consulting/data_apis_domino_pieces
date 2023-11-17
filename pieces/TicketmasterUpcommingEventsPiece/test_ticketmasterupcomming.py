from domino.testing import piece_dry_run
import os


def test_ticketmaster_upcomming():
    TICKETMASTER_API_KEY = os.environ.get("TICKETMASTER_API_KEY", None)
    if not TICKETMASTER_API_KEY:
        raise Exception("TICKETMASTER_API_KEY is required.")
    input_data = dict(
        max_number_of_events=10,
        keyword="music",
        end_date="2025-12-31",
        city="San Francisco",
    )
    piece_output = piece_dry_run(
        piece_name="TicketmasterUpcommingEventsPiece",
        input_data=input_data,
        secrets_data=dict(
            TICKETMASTER_API_KEY=TICKETMASTER_API_KEY
        ),
    )
    assert piece_output.get("events") is not None
    assert len(piece_output.get("events", [])) < 11
    for e in piece_output.get("events", []):
        assert e.get("name") is not None
        assert e.get("event_date") is not None
        assert e.get("event_location") is not None
    assert piece_output.get("results_formatted") is not None
