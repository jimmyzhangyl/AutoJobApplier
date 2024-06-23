# backend/tests/sample_data.py

valid_filter = {
    "titleIncludes": ["Software"],
    "titleExcludes": ["Manager"],
    "locationIncludes": ["All Canberra ACT"],
    "locationExcludes": ["Sydney NSW"],
    "typeExcludes": ["Part-time"],
    "descriptionIncludes": ["Python", "Java"],
    "descriptionExcludes": ["C++", "C#"],
    "jobSource": ["Seek"],
    "daysListed": 1,
}

sample_response = [
    {
        "id": 1,
        "title": "Software Engineer",
        "location": "Canberra ACT",
        "description": "Develop web applications.",
        "listedDate": "2023-12-01",
        "type": "Full-time",
        "quickApplySupported": True,
        "url": "http://example.com/job/1",
    },
    {
        "id": 2,
        "title": "Software Engineer 2",
        "location": "Sydney NSW",
        "description": "Develop mobile applications.",
        "listedDate": "2024-12-01",
        "type": "Contract",
        "quickApplySupported": False,
        "url": "http://example.com/job/2",
    },
]
