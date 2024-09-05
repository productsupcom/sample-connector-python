import sys
import connector.data_source
import connector.data_service


if __name__ == '__main__':
    if len(sys.argv) < 1:
        sys.exit(1)

    if len(sys.argv) > 1:
        if len(sys.argv) > 2 and sys.argv[2] == '--health-check':
            sys.exit()

        if sys.argv[1] == 'data-source':
            connector.data_source.failed_call_to_container_api()
            connector.data_source.append_sample_products()
            connector.data_source.log_something()
            connector.data_source.read_env_var_and_exit()
            sys.exit()

        if sys.argv[1] == 'data-service':
            connector.data_service.data_service()

            sys.exit()
