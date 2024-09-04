import sys
import connector.sample_data
import connector.data_service


if __name__ == '__main__':
    if len(sys.argv) < 1:
        sys.exit(1)

    if len(sys.argv) > 1:
        if len(sys.argv) > 2 and sys.argv[2] == '--health-check':
            sys.exit()

        if sys.argv[1] == 'data-source':
            connector.sample_data.failed_call_to_container_api()
            connector.sample_data.append_sample_products()
            connector.sample_data.log_something()
            connector.sample_data.read_env_var_and_exit()
            sys.exit()

        if sys.argv[1] == 'data-service':
            connector.data_service.data_service()

            sys.exit()
