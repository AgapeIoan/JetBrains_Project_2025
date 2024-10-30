import java.io.BufferedReader
import java.io.InputStreamReader
import kotlin.random.Random

const val MAX_RANDOM_NUMBER = 100_000

fun processMessage(message: String): String {
    val commands = mapOf(
        "Hi" to "Hi",
        "GetRandom" to Random.nextInt(1, MAX_RANDOM_NUMBER).toString(),
        "Shutdown" to "shutdown"
    )
    return commands[message] ?: ""
}

fun sendMessage(message: String) {
    if (message.isEmpty()) return
    println(message)
    System.out.flush()
}

fun messageSequence(reader: BufferedReader): Sequence<String> = sequence {
    while (true) {
        val message = reader.readLine()?.trim() ?: break
        yield(message)
    }
}

fun main() {
    val reader = BufferedReader(InputStreamReader(System.`in`))
    val messages = messageSequence(reader)

    for (message in messages) {
        val response = processMessage(message)
        sendMessage(response)

        if (message == "Shutdown") {
            sendMessage("Program A: Shutting down.")
            break
        }
    }
}