from cognite.client import CogniteClient, config, global_config
from cognite.client.data_classes.data_modeling import NodeId, ViewId
from sdk import get_client  # custom import

client = get_client()

## creating spaces
def create_space():
    from cognite.client.data_classes.data_modeling import SpaceApply
    spaces = SpaceApply(space="sp_inst_abhishek_test", description="Space created for testing",
                        name="Abhishek Test Space")
    res = client.data_modeling.spaces.apply(spaces)

    print(res)
    print("space created")
    return res


## creating containers
def create_container():
    from cognite.client.data_classes.data_modeling import (ContainerApply, ContainerProperty, Text, Float64)
    container = ContainerApply(
        space="sp_inst_abhishek_test",
        external_id="abhishek_test",  # container name
        properties={
            "name": ContainerProperty(type=Text, name="name"),
            "numbers": ContainerProperty(
                type=Float64(is_list=True, max_list_size=200),
                description="very important numbers",
            ),
        },
    ),
    res = client.data_modeling.containers.apply(container)
    print("container created.....")
    return res


## creating views  -- we will have to create a view also if the container & view are of same properties & fields!
def create_view():
    from cognite.client.data_classes.data_modeling import ViewApply, MappedPropertyApply, ContainerId
    views = [
        ViewApply(
            space="sp_inst_abhishek_test",
            external_id="abhishek_test",
            version="v1",
            properties={
                "title": MappedPropertyApply(  # this is just another name for your container property
                    container=ContainerId("sp_inst_abhishek_test", "abhishek_test"),
                    container_property_identifier="name",
                ),
                "sequence": MappedPropertyApply(  # this is just another name for your container property
                    container=ContainerId("sp_inst_abhishek_test", "abhishek_test"),
                    container_property_identifier="numbers",
                ),
            }
        )
    ]
    res = client.data_modeling.views.apply(views)
    print("view created....")
    return res


## creating data models -- just a logical grouping of views! (views are tied up to containers)
def create_data_model():
    from cognite.client.data_classes.data_modeling import DataModelApply
    data_models = DataModelApply(space="sp_inst_abhishek_test", external_id="data_model_abhishek_test", version="v1",
                                 name="Abhishek test data model",
                                 views=[ViewId(space="sp_inst_abhishek_test",
                                               external_id="abhishek_test",
                                               version="v1")])
    res = client.data_modeling.data_models.apply(data_models)

    print("data model created......")
    return res


## creating instances -- inserting the main time series data in to CDM
def create_instances():
    from cognite.client.data_classes.data_modeling import EdgeApply, NodeOrEdgeData, NodeApply, ViewId
    array_nodes = []
    for i in range(10):
        node = NodeApply(
            space="sp_inst_abhishek_test", external_id=f"abhishek_test_node_{i}",
            sources=[
                NodeOrEdgeData(
                    ViewId(space="sp_inst_abhishek_test",
                           external_id="abhishek_test",
                           version="v1"),
                    {"title": f"Instance Title {i}", "sequence": [2025 * i]}
                )
            ]
        )
        array_nodes.append(node)
    print(array_nodes)

    # first we created array containing all instances of nodes (data rows), then inserted into CDM.
    res = client.data_modeling.instances.apply(array_nodes)
    print("instance created....")
    return res


def create_time_series():
    from cognite.client.data_classes import TimeSeriesWrite, TimeSeries
    # ts = client.time_series.create(TimeSeriesWrite(name="my_ts_tag1", data_set_id=123, external_id="my_ts_tag1"))
    ts = client.time_series.create(TimeSeries(name="my_test_tag1",
                                              description='Random test data points',
                                              is_string=False, is_step=True,
                                              external_id="my_test_tag1", ))

    print("time series created successfully....")


def insert_data_points():
    from cognite.client.data_classes import StatusCode
    from datetime import datetime, timezone
    import numpy as np
    # client = CogniteClient()
    datapoints = [
        (datetime(2018, 1, 9, tzinfo=timezone.utc), None, StatusCode.Bad),
        # you can insert null data using status code as Bad, or simply drop that
        # (datetime(2018,1,6, tzinfo=timezone.utc), 2000, StatusCode.Good),
        # (datetime(2018,1,7, tzinfo=timezone.utc), 3000, StatusCode.Good),  # StatusCode.Uncertain, StatusCode.Bad
        # (datetime(2018,1,8, tzinfo=timezone.utc), None, StatusCode.Bad),
    ]
    # client.time_series.data.insert(datapoints, instance_id=NodeId(space="sp_inst_abhishek_test", external_id="my_test_tag1"))  ## give the node external id you want to insert the data.
    client.time_series.data.insert(datapoints,
                                   external_id="my_test_tag1")  ## give the node external id you want to insert the data.

    print("Inserted all the datapoints successfully....")


# create_space()
# create_container()
# create_view()
# create_data_model()
# create_instances()  # main data insertion ... tags insertion
# create_time_series()
insert_data_points()