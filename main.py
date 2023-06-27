import sys
import connector.sample_data


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--health-check':
        sys.exit()
    connector.sample_data.failed_call_to_container_api()
    connector.sample_data.append_sample_products()
    connector.sample_data.log_something()
    connector.sample_data.read_env_var_and_exit()
