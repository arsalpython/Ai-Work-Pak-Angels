import streamlit as st
from datetime import date, timedelta
from statistics import mean

st.set_page_config(
    page_title="PawPath | Dog Walking",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# DEMO DATA
# ------------------------------------------------------------
WALKERS = [
    {
        "name": "Maya",
        "rating": 4.9,
        "reviews": 128,
        "price": 18,
        "distance": 0.8,
        "experience": 5,
        "completed": 612,
        "available": True,
        "specialty": "Energetic dogs",
        "bio": "Calm, reliable walker who loves long park walks and high-energy breeds.",
    },
    {
        "name": "Daniel",
        "rating": 4.8,
        "reviews": 96,
        "price": 16,
        "distance": 1.3,
        "experience": 4,
        "completed": 431,
        "available": True,
        "specialty": "Puppies",
        "bio": "Patient and playful, with extra experience handling puppies and young dogs.",
    },
    {
        "name": "Sofia",
        "rating": 5.0,
        "reviews": 74,
        "price": 22,
        "distance": 2.1,
        "experience": 7,
        "completed": 804,
        "available": True,
        "specialty": "Senior dogs",
        "bio": "Experienced walker focused on gentle exercise, senior dogs, and special routines.",
    },
    {
        "name": "Adam",
        "rating": 4.7,
        "reviews": 61,
        "price": 14,
        "distance": 2.8,
        "experience": 3,
        "completed": 278,
        "available": False,
        "specialty": "Large breeds",
        "bio": "Confident with larger dogs and structured walks. Available most evenings.",
    },
    {
        "name": "Lina",
        "rating": 4.9,
        "reviews": 111,
        "price": 20,
        "distance": 1.7,
        "experience": 6,
        "completed": 690,
        "available": True,
        "specialty": "Shy dogs",
        "bio": "Gentle, attentive walker who builds trust with nervous and shy dogs.",
    },
]


# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
def init_state():
    today = date.today()

    if "owner_name" not in st.session_state:
        st.session_state.owner_name = "Alex"

    if "pet" not in st.session_state:
        st.session_state.pet = {
            "name": "Buddy",
            "breed": "Golden Retriever",
            "age": 4,
            "size": "Large",
            "notes": "Friendly, loves parks and carries a tennis ball.",
        }

    if "bookings" not in st.session_state:
        st.session_state.bookings = [
            {
                "id": "BK-1001",
                "walker": "Maya",
                "pet": "Buddy",
                "date": today - timedelta(days=2),
                "time": "5:00 PM",
                "duration": 30,
                "price": 18,
                "status": "Completed",
                "payment": "Paid",
            }
        ]

    if "reviews" not in st.session_state:
        st.session_state.reviews = [
            {
                "walker": "Daniel",
                "rating": 5,
                "behaviour": 5,
                "quality": 5,
                "comment": "Very friendly, punctual and careful with the dog.",
                "date": today - timedelta(days=6),
            }
        ]

    if "visit_dates" not in st.session_state:
        st.session_state.visit_dates = {
            today - timedelta(days=3),
            today - timedelta(days=2),
            today - timedelta(days=1),
            today,
        }
    else:
        st.session_state.visit_dates.add(today)

    if "selected_walker" not in st.session_state:
        st.session_state.selected_walker = None


def current_streak():
    dates = set(st.session_state.visit_dates)
    cursor = date.today()
    streak = 0

    while cursor in dates:
        streak += 1
        cursor -= timedelta(days=1)

    return streak


def get_walker(name):
    for walker in WALKERS:
        if walker["name"] == name:
            return walker
    return None


init_state()

# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------
st.title("🐾 PawPath")
st.subheader("Trusted walks. Happier dogs.")
st.write(
    f"Welcome back, **{st.session_state.owner_name}**. "
    "Find highly rated dog walkers, book a walk, track your streak, "
    "and review walkers after completed bookings."
)

st.divider()

tabs = st.tabs(
    [
        "🏠 Home",
        "🐕 Find Walkers",
        "📅 My Bookings",
        "🔥 Streak",
        "⭐ Reviews",
        "🦴 My Pet",
        "🛡️ Safety",
    ]
)

# ------------------------------------------------------------
# HOME
# ------------------------------------------------------------
with tabs[0]:
    streak = current_streak()
    completed_count = sum(
        1 for booking in st.session_state.bookings
        if booking["status"] == "Completed"
    )
    upcoming_count = sum(
        1 for booking in st.session_state.bookings
        if booking["status"] == "Upcoming"
    )
    avg_rating = (
        mean([review["rating"] for review in st.session_state.reviews])
        if st.session_state.reviews else 0
    )

    a, b, c, d = st.columns(4)
    a.metric("🔥 Current streak", f"{streak} days")
    b.metric("🐕 Completed walks", completed_count)
    c.metric("📅 Upcoming walks", upcoming_count)
    d.metric("⭐ Your avg. rating", f"{avg_rating:.1f}" if avg_rating else "—")

    st.write("")
    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.subheader(f"🐶 {st.session_state.pet['name']}'s routine")
            st.write(
                "A reliable walk helps your dog stay active and gives you "
                "peace of mind when your day gets busy."
            )
            st.info("Recommended: book a trusted walker for a 30–60 minute walk.")

    with right:
        with st.container(border=True):
            st.subheader("💛 Why owners use PawPath")
            st.write("✅ Save time finding a walker")
            st.write("⭐ Compare ratings and experience")
            st.write("💳 See the price before booking")
            st.write("🐾 Keep the dog's routine consistent")
            st.write("🧘 Reduce stress when you're busy")

    st.subheader("🌟 Top walkers")
    top_walkers = sorted(WALKERS, key=lambda w: w["rating"], reverse=True)[:3]
    cols = st.columns(3)

    for col, walker in zip(cols, top_walkers):
        with col:
            with st.container(border=True):
                st.subheader(f"🐕 {walker['name']}")
                st.write(f"⭐ **{walker['rating']}** · {walker['reviews']} reviews")
                st.write(f"📍 {walker['distance']} km away")
                st.write(f"💵 **${walker['price']}** / 30 minutes")
                st.caption(walker["specialty"])

# ------------------------------------------------------------
# FIND WALKERS
# ------------------------------------------------------------
with tabs[1]:
    st.header("Find your perfect walker")

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        min_rating = st.selectbox(
            "Minimum rating",
            [4.0, 4.5, 4.7, 4.8, 4.9, 5.0],
            index=2,
        )

    with f2:
        max_price = st.selectbox(
            "Maximum price",
            [15, 20, 25, 30],
            index=2,
            format_func=lambda x: f"${x} / 30 min",
        )

    with f3:
        max_distance = st.selectbox(
            "Maximum distance",
            [1, 2, 3, 5, 10],
            index=3,
            format_func=lambda x: f"{x} km",
        )

    with f4:
        availability = st.selectbox(
            "Availability",
            ["Available only", "Show all"],
        )

    available_only = availability == "Available only"

    filtered = [
        walker for walker in WALKERS
        if walker["rating"] >= min_rating
        and walker["price"] <= max_price
        and walker["distance"] <= max_distance
        and (walker["available"] or not available_only)
    ]

    st.caption(f"{len(filtered)} walker(s) match your filters.")

    for walker in filtered:
        with st.container(border=True):
            info, action = st.columns([4, 1])

            with info:
                status = "🟢 Available" if walker["available"] else "⚪ Unavailable"
                st.subheader(f"🐾 {walker['name']}")
                st.write(
                    f"⭐ **{walker['rating']}** ({walker['reviews']} reviews) · "
                    f"📍 {walker['distance']} km · {status}"
                )
                st.write(
                    f"**{walker['experience']} years experience** · "
                    f"{walker['completed']} completed walks"
                )
                st.write(f"💵 **${walker['price']} / 30 minutes**")
                st.caption(f"Specialty: {walker['specialty']}")
                st.write(walker["bio"])

            with action:
                if st.button(
                    f"Book {walker['name']}",
                    key=f"book_{walker['name']}",
                    type="primary",
                    disabled=not walker["available"],
                    use_container_width=True,
                ):
                    st.session_state.selected_walker = walker["name"]

    if st.session_state.selected_walker:
        walker = get_walker(st.session_state.selected_walker)

        st.divider()
        st.subheader(f"Book {walker['name']}")

        with st.form("booking_form"):
            c1, c2, c3 = st.columns(3)

            with c1:
                walk_date = st.date_input(
                    "Walk date",
                    value=date.today() + timedelta(days=1),
                    min_value=date.today(),
                )

            with c2:
                walk_time = st.selectbox(
                    "Start time",
                    [
                        "7:00 AM",
                        "9:00 AM",
                        "12:00 PM",
                        "3:00 PM",
                        "5:00 PM",
                        "7:00 PM",
                    ],
                )

            with c3:
                duration = st.selectbox(
                    "Duration",
                    [30, 60],
                    format_func=lambda x: f"{x} minutes",
                )

            notes = st.text_area(
                "Notes for the walker",
                value=st.session_state.pet["notes"],
            )

            total = walker["price"] * (duration // 30)
            st.info(f"Demo total: **${total}**. No real payment is collected.")

            submit = st.form_submit_button(
                "Confirm & Demo Pay",
                type="primary",
                use_container_width=True,
            )

        if submit:
            booking_id = f"BK-{1000 + len(st.session_state.bookings) + 1}"

            st.session_state.bookings.append(
                {
                    "id": booking_id,
                    "walker": walker["name"],
                    "pet": st.session_state.pet["name"],
                    "date": walk_date,
                    "time": walk_time,
                    "duration": duration,
                    "price": total,
                    "status": "Upcoming",
                    "payment": "Paid (Demo)",
                    "notes": notes,
                }
            )

            st.session_state.selected_walker = None
            st.success(
                f"Booking confirmed with {walker['name']} for "
                f"{walk_date.strftime('%d %b %Y')} at {walk_time}."
            )

# ------------------------------------------------------------
# BOOKINGS
# ------------------------------------------------------------
with tabs[2]:
    st.header("My bookings")

    if not st.session_state.bookings:
        st.info("No bookings yet.")

    for booking in sorted(
        st.session_state.bookings,
        key=lambda x: x["date"],
        reverse=True,
    ):
        with st.container(border=True):
            st.subheader(
                f"{'✅' if booking['status'] == 'Completed' else '📅'} "
                f"{booking['walker']} with {booking['pet']}"
            )
            st.write(
                f"**{booking['date'].strftime('%A, %d %B %Y')}** · "
                f"{booking['time']} · {booking['duration']} minutes"
            )
            st.write(
                f"💵 ${booking['price']} · {booking['payment']} · "
                f"**{booking['status']}**"
            )
            st.caption(f"Booking ID: {booking['id']}")

            if booking["status"] == "Upcoming":
                if st.button(
                    "Mark walk completed",
                    key=f"complete_{booking['id']}",
                ):
                    booking["status"] = "Completed"
                    st.success("Walk completed. You can now review this walker.")
                    st.rerun()

# ------------------------------------------------------------
# STREAK
# ------------------------------------------------------------
with tabs[3]:
    streak = current_streak()

    st.header("🔥 PawPath streak")
    st.metric("Current streak", f"{streak} days")

    if streak >= 30:
        st.success("🏅 PawPath Champion — 30+ days!")
    elif streak >= 7:
        st.success("🔥 Routine Builder — 7+ days!")
    elif streak >= 3:
        st.info("🐾 Getting Started — 3+ days!")
    else:
        st.info("Use PawPath daily to grow your streak.")

    st.subheader("Last 7 days")
    cols = st.columns(7)

    for index, col in enumerate(cols):
        day = date.today() - timedelta(days=6-index)
        active = day in st.session_state.visit_dates

        with col:
            with st.container(border=True):
                st.write("🔥" if active else "○")
                st.write(f"**{day.strftime('%a')}**")
                st.caption(day.strftime("%d %b"))

    st.warning(
        "MVP note: streak data currently lives in session memory. "
        "A database will be added later for permanent user accounts."
    )

# ------------------------------------------------------------
# REVIEWS
# ------------------------------------------------------------
with tabs[4]:
    st.header("⭐ Review a previous walker")

    completed_walkers = sorted(
        {
            booking["walker"]
            for booking in st.session_state.bookings
            if booking["status"] == "Completed"
        }
    )

    if completed_walkers:
        with st.form("review_form", clear_on_submit=True):
            walker_name = st.selectbox("Walker", completed_walkers)
            overall = st.selectbox("Overall rating", [5, 4, 3, 2, 1])
            behaviour = st.selectbox(
                "Behaviour & professionalism",
                [5, 4, 3, 2, 1],
            )
            quality = st.selectbox(
                "Walk quality & care",
                [5, 4, 3, 2, 1],
            )
            comment = st.text_area(
                "Your review",
                placeholder="Was the walker punctual, friendly and careful?",
            )

            review_submit = st.form_submit_button(
                "Submit review",
                type="primary",
            )

        if review_submit:
            if len(comment.strip()) < 5:
                st.warning("Please write a short review.")
            else:
                st.session_state.reviews.insert(
                    0,
                    {
                        "walker": walker_name,
                        "rating": overall,
                        "behaviour": behaviour,
                        "quality": quality,
                        "comment": comment.strip(),
                        "date": date.today(),
                    },
                )
                st.success(f"Review added for {walker_name}.")
    else:
        st.info("Complete a walk before leaving a review.")

    st.subheader("Previous reviews")

    for review in st.session_state.reviews:
        with st.container(border=True):
            st.write(f"### {review['walker']} · {'⭐' * review['rating']}")
            st.caption(review["date"].strftime("%d %b %Y"))
            st.write(
                f"Behaviour: **{review['behaviour']}/5** · "
                f"Quality: **{review['quality']}/5**"
            )
            st.write(review["comment"])

# ------------------------------------------------------------
# PET PROFILE
# ------------------------------------------------------------
with tabs[5]:
    st.header("🦴 My pet")

    with st.form("pet_form"):
        c1, c2 = st.columns(2)

        with c1:
            pet_name = st.text_input(
                "Dog name",
                value=st.session_state.pet["name"],
            )
            breed = st.text_input(
                "Breed",
                value=st.session_state.pet["breed"],
            )
            age = st.number_input(
                "Age",
                min_value=0,
                max_value=25,
                value=int(st.session_state.pet["age"]),
            )

        with c2:
            size_options = ["Small", "Medium", "Large", "Extra Large"]
            size = st.selectbox(
                "Size",
                size_options,
                index=size_options.index(st.session_state.pet["size"]),
            )
            notes = st.text_area(
                "Care notes",
                value=st.session_state.pet["notes"],
            )

        save_pet = st.form_submit_button(
            "Save pet profile",
            type="primary",
        )

    if save_pet:
        st.session_state.pet = {
            "name": pet_name.strip() or "Buddy",
            "breed": breed.strip() or "Mixed breed",
            "age": int(age),
            "size": size,
            "notes": notes.strip(),
        }
        st.success("Pet profile saved.")

    with st.container(border=True):
        st.subheader(f"🐶 {st.session_state.pet['name']}")
        st.write(
            f"{st.session_state.pet['breed']} · "
            f"{st.session_state.pet['age']} years old · "
            f"{st.session_state.pet['size']}"
        )
        st.write("**Walker notes**")
        st.write(st.session_state.pet["notes"] or "No notes added.")

# ------------------------------------------------------------
# SAFETY
# ------------------------------------------------------------
with tabs[6]:
    st.header("🛡️ Trust & safety")

    c1, c2, c3 = st.columns(3)

    with c1:
        with st.container(border=True):
            st.subheader("🪪 Verified profiles")
            st.write(
                "Future production versions should verify walker "
                "identity, email and phone."
            )

    with c2:
        with st.container(border=True):
            st.subheader("⭐ Transparent reviews")
            st.write(
                "Owners can review behaviour and walk quality after "
                "a completed booking."
            )

    with c3:
        with st.container(border=True):
            st.subheader("🚨 Support & reporting")
            st.write(
                "Future versions should include emergency contacts, "
                "incident reporting and customer support."
            )

    st.warning(
        "This is a learning MVP. Real payments, GPS tracking, "
        "authentication, background checks and a persistent database "
        "will be added in later versions."
    )

st.divider()
st.caption(
    "PawPath MVP · Python + Streamlit · Built for product learning and validation"
)
