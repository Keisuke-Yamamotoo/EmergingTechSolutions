
def create_datastore_entity(projectId, datastore_data: dict):   
 except client_exceptions.ClientError as error:
            if error.status == 403:  # Check if correct access was provided.
                print("[FATAL ERROR] To use Google Cloud Datastore, Enable it on your GCP Project and login successfully!")
                return {'status': 0, 'message': "Forbidden access!!"}
            else:
                raise
        except:
            global_routes.Halt_Runner(19, {"Datastore Error": "working with Google Cloud Datastore!!"})
        key = client.key(kind, datastore_data[key_to_use])
        client.put(key, data=datastore_data)


from google.cloud import ndb

class GAEService:    
    


    @staticmethod
    def entity_put(ndb_key, data_dict):
        entity = GAE_Entity(id=ndb_key, **data_dict)
        entity.put()
       

    @staticmethod
    def entity_get(ndb_key):
        entity = GAE_Entity.get_by_id(ndb_key)
        if entity:
            return entity
        else:
            return None
           

    @staticmethod
    def release_multicloud_lock(pubsub_key:str,gae_data:dict,action_by:str,channel:str,dataflow_key:str):
        obj = '/req.' + pubsub_key
        gae_data['channel'] = channel
        gae_data['action_by'] = action_by
        gae_data['release_by'] = action_by
        gae_data['release_date'] = datetime.now()
        if gae_data['status'] == 'WAITING':
            GAE_Scheduler.delete_from_task_queue(obj)
        GAEService.entity_put(obj,gae_data)
        entity = GAEService.entity_get('/dataflow.' + dataflow_key)
        if entity is None:
            return jsonify({'error': f'Key Must Be pre-populated of {dataflow_key}'}, {'status': 0})
        entity.apply_on_ship = True
        #entity.updated = datetime.now()
        dataflow_obj = '/dataflow.'+dataflow_key
        GAEService.entity_put(dataflow_obj,entity)
        return {'status': 1}
    

    @staticmethod
    def release_lock(pubsub_key:str,gae_data:dict,action_by:str,channel:str = ''):
        ''' Functionality to release the lock
                :param pubsub_key:- pubsub key
                :param gae_data:- Access data to be release
                :param action_by:- Person who is try to release the lock
                :param channel:- Channel (Default Empty String)

                :return: JSON Response with Status (1,0) 
        '''
        obj = '/req.' + pubsub_key
        gae_data['channel'] = channel
        gae_data['action_by'] = action_by
        gae_data['release_by'] = action_by
        gae_data['release_date'] = datetime.now()
        if gae_data['status'] == 'WAITING':
            GAE_Scheduler.delete_from_task_queue(obj)
        GAEService.entity_put(obj,gae_data)
        return {'status': 1}    
      
      
      
   
    @staticmethod
    def set_cloud_config(project='ind-cloud-anything-1397', region='us-central1', project_number=None, service_account_info=None):
        if project_number == None:
            project_number=PROJECT_NUMBER
        client_ndd = ndb.Client(project_number)
        if service_account_info:
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            client_ndd = ndb.Client(project_number,credentials).from_service_account_info(service_account_info)
        ndb.setup( project=project,region=region, client=client_ndd)
