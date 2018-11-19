from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb5lVL11vkfQ8CK9JPU4TuIFOxT38OQZb8GM_fi7EpUcWgFIyH8v_hJ0RUX_72zSqV0wadGzVnabn_rF20ZNiDSnhXl_sctkP-L' \
          b'5XJuW2XSgR2IrqnZooayF5oJ5OlrkpVPzwz7IlXc_nY8eSqBLlmc8Op5cNJ7W-wNHJJgc0ldE8QKnmsx1pKSZaNx_q7BzTNriug'


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
