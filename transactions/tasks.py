# transactions/tasks.py
from celery import shared_task
from .models import Transaction
from project.celery import app
@shared_task
def process_transaction(transaction_id):
    try:
        # Retrieve the transaction from the database using the provided ID
        transaction = Transaction.objects.get(pk=transaction_id)

        # Your processing logic here
        # For example, print the transaction details
        print(f"Processing transaction: {transaction}")

        # If needed, perform additional processing or update the transaction status
        # ...

        # Once processing is complete, you can log or return a result
        return f"Transaction {transaction_id} processed successfully"
    except Transaction.DoesNotExist:
        print(f"Transaction with ID {transaction_id} does not exist")
        return f"Transaction {transaction_id} not found"
    except Exception as e:
        print(f"Error processing transaction {transaction_id}: {e}")
        # You may want to log the error or handle it appropriately
        return f"Error processing transaction {transaction_id}: {e}"
    return transaction_id
