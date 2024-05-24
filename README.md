# Amazon Location Service Plugin

Read this in other languages: [Japanese](./README_ja.md)

![logo](img/logo.png)

This plugin uses the functionality of Amazon Location Service in QGIS.  

- [QGIS](https://qgis.org)  
- [Amazon Location Service](https://aws.amazon.com/location)  

## QGIS Python Plugins Repository

[Amazon Location Service Plugin](https://plugins.qgis.org/plugins/location_service)  

## blog

## Usage

### Building an Amazon Location Service Resources

![location-service](img/location-service.png)

Select from the following to build your resources

- AWS Management Console
- AWS CDK
- AWS CloudFormation

[Building an Amazon Location Service Resources with AWS CDK and AWS CloudFormation](https://dev.to/aws-heroes/building-an-amazon-location-service-resources-with-aws-cdk-and-aws-cloudformation-22jj)  
[dayjournal memo - Amazon Location Service](https://memo.dayjournal.dev/tags/amazon-location-service/)  

### Install QGIS Plugin

![plugin](img/plugin.png)

1. Select "Plugins" → "Manage and Install Plugins..."
2. Search for "Amazon Location Service"

Plugins can also be installed by loading a [zip file](https://github.com/dayjournal/qgis-amazonlocationservice-plugin/releases).

### Menu

![menu](img/menu.png)

- Config: Set each resource name and API key
- Map: Map display function
- Place: Geocoding function
- Routes: Routing function
- Terms: Display Terms of Use page

### Config Function

![config](img/config.png)

1. Click the “Config” menu
2. Set each resource name and API key
    - Region: ap-xxxxx
    - API Key: v1.public.xxxxx
    - Map Name: Mapxxxxx
    - Place Name: Placexxxxx
    - Routes Name: Routesxxxxx
3. Click “Save“

### Map Function

![map](img/map.gif)

1. Click the “Map” menu
2. Select “Map Name“
3. Click “Add“
4. The map is displayed as a layer

※ As of May 2024, only one style can be displayed.

### Place Function

![place](img/place.gif)

1. Click the “Place” menu
2. Select “Select Function“
3. Click “Get Location“
4. Click on the location you wish to search
5. Click “Search”
6. Search results are displayed in layers

※ As of May 2024, only ”SearchPlaceIndexForPosition” is available.

### Routes Function

![routes](img/routes.gif)

1. Click the “Routes” menu
2. Select “Select Function“
3. Click “Get Location(Starting Point)“
4. Click the starting point
5. Click “Get Location(End Point)“
6. Click on the endpoint
7. Click “Search”
8. Search results are displayed in layers

※ As of May 2024, only ”CalculateRoute” is available.

### Terms Function

1. Click the “Terms” menu
2. The Terms of Use page will be displayed in your browser.

### Terms

[AWS Service Terms](https://aws.amazon.com/jp/service-terms)

Amazon Location Service has terms of use for data usage. Please check the section “82. Amazon Location Service” and use the service at your own risk. The developer is not responsible for any damages that may occur in connection with the use of this service.  

When using HERE as a provider, in addition to the basic terms and conditions, you may not.  

a. Store or cache any Location Data for Japan, including any geocoding or reverse-geocoding results.  
b. Layer routes from HERE on top of a map from another third-party provider, or layer routes from another third-party provider on top of maps from HERE.  

## License

Python modules are released under the GNU General Public License v2.0

Copyright (c) 2024 Yasunori Kirimoto
