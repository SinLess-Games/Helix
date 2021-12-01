/*
 * Copyright (c) 2015 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
// [START all]

using CommandLine;
using Google.Apis.Auth.OAuth2;
using Google.Apis.Services;
using Google.Apis.Storage.v1;
using Google.Cloud.Language.V1;
using Google.Cloud.Storage.V1;
using Grpc.Auth;
using System;
using System.Net.Http;
using Google.Api.Gax.ResourceNames;
using Google.Cloud.SecretManager.V1;


private string ProjectId = "helix-ai-318319";
private string api_key = "AIzaSyD8kvll4QoWXAM40OcdezcgT9D2XGD_Prc";


public object AuthImplicit(string projectId)
{
    // If you don't specify credentials when constructing the client, the
    // client library will look for credentials in the environment.
    var credential = GoogleCredential.GetApplicationDefault();
    var storage = StorageClient.Create(credential);
    // Make an authenticated API request.
    var buckets = storage.ListBuckets(projectId);
    foreach (var bucket in buckets)
    {
        Console.WriteLine(bucket.Name);
    }
    return null;
}