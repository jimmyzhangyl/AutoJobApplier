import pytest
from server.models.job_filter_model import JobFilter


def test_job_filter_valid():
    job_filter = JobFilter(
        daysListed=3,
        titleIncludes=["Developer"],
        titleExcludes=["Manager"],
        locationIncludes=["New York"],
        locationExcludes=["Los Angeles"],
        typeExcludes=["Full-time"],
        descriptionIncludes=["Python"],
        descriptionExcludes=["Java"],
        jobSource=["LinkedIn"],
    )
    assert job_filter.daysListed == 3
    assert job_filter.titleIncludes == ["Developer"]
    assert job_filter.titleExcludes == ["Manager"]
    assert job_filter.locationIncludes == ["New York"]
    assert job_filter.locationExcludes == ["Los Angeles"]
    assert job_filter.typeExcludes == ["Full-time"]
    assert job_filter.descriptionIncludes == ["Python"]
    assert job_filter.descriptionExcludes == ["Java"]
    assert job_filter.jobSource == ["LinkedIn"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("titleIncludes", "NotAList"),
        ("titleExcludes", "NotAList"),
        ("locationIncludes", "NotAList"),
        ("locationExcludes", "NotAList"),
        ("typeExcludes", "NotAList"),
        ("descriptionIncludes", "NotAList"),
        ("descriptionExcludes", "NotAList"),
        ("jobSource", "NotAList"),
        ("daysListed", "NotAnInt"),
    ],
)
def test_job_filter_invalid(field, value):
    with pytest.raises(TypeError):
        JobFilter(**{field: value})


def test_job_filter_invalid_daysListed():
    with pytest.raises(TypeError):
        JobFilter(daysListed="NotAnInt")
