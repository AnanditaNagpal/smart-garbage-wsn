#include "contiki.h"
#include "sys/node-id.h"
#include "net/routing/routing.h"
#include "net/routing/rpl-lite/rpl.h"
#include "net/routing/rpl-lite/rpl-neighbor.h"
#include "random.h"
#include "net/netstack.h"
#include "net/ipv6/simple-udp.h"
#include <stdint.h>
#include <inttypes.h>

#include "sys/log.h"
#define LOG_MODULE "App"
#define LOG_LEVEL LOG_LEVEL_INFO

#define WITH_SERVER_REPLY  1
#define UDP_CLIENT_PORT	8765
#define UDP_SERVER_PORT	5678

#define ADAPTIVE_REPORTING 0
#define SEND_INTERVAL		  (5 * CLOCK_SECOND)


/* Synthetic resident deposits, independent of radio reporting. */
static unsigned bin_fill;

static unsigned
simulated_fill(void)
{
  return bin_fill;
}

PROCESS(waste_process, "Synthetic resident deposits");

PROCESS_THREAD(waste_process, ev, data)
{
  static struct etimer deposit_timer;
  static unsigned amount;
  static unsigned accepted;

  PROCESS_BEGIN();

  bin_fill = (node_id * 13U) % 40U;
  LOG_INFO("BIN_INIT bin=%u fill=%u\n", (unsigned)node_id, bin_fill);

  etimer_set(&deposit_timer, (8 + node_id % 9) * CLOCK_SECOND);

  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&deposit_timer));

    amount = 6U + (node_id % 5U);
    accepted = amount > 100U - bin_fill ? 100U - bin_fill : amount;
    bin_fill += accepted;

    LOG_INFO("BIN_DEPOSIT bin=%u offered=%u accepted=%u fill=%u\n",
             (unsigned)node_id, amount, accepted, bin_fill);

    etimer_set(&deposit_timer, (12 + node_id % 7) * CLOCK_SECOND);
  }

  PROCESS_END();
}

/* Synthetic scheduled visits, not gateway-controlled dispatch.
 * One route repeats every 360 seconds; bin slots are 8 seconds apart.
 */
PROCESS(collection_process, "Scheduled collection visits");

PROCESS_THREAD(collection_process, ev, data)
{
  static struct etimer collection_timer;
  static unsigned before;

  PROCESS_BEGIN();

  etimer_set(&collection_timer,
            (240UL + 8UL * (node_id - 2U)) * CLOCK_SECOND);

  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&collection_timer));

    before = bin_fill;
    LOG_INFO("TRUCK_VISIT bin=%u fill=%u\n",
             (unsigned)node_id, before);

    if(before >= 80U) {
      bin_fill = 0;
      LOG_INFO("BIN_COLLECTION bin=%u before=%u removed=%u fill=0\n",
               (unsigned)node_id, before, before);
    } else {
      LOG_INFO("TRUCK_SKIP bin=%u fill=%u reason=below_threshold\n",
               (unsigned)node_id, before);
    }

    etimer_set(&collection_timer, 360UL * CLOCK_SECOND);
  }

  PROCESS_END();
}

/* Record the preferred parent at each application send. */
static void
log_rpl_parent(void)
{
  rpl_nbr_t *parent = curr_instance.dag.preferred_parent;
  uip_ipaddr_t *addr = parent != NULL ?
    rpl_neighbor_get_ipaddr(parent) : NULL;

  if(addr != NULL) {
    LOG_INFO("RPL_PARENT node=%u parent=", (unsigned)node_id);
    LOG_INFO_6ADDR(addr);
    LOG_INFO_("\n");
  }
}

static struct simple_udp_connection udp_conn;
static uint32_t rx_count = 0;

/*---------------------------------------------------------------------------*/
PROCESS(udp_client_process, "UDP client");
AUTOSTART_PROCESSES(&waste_process, &collection_process, &udp_client_process);
/*---------------------------------------------------------------------------*/
static void
udp_rx_callback(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{

  LOG_INFO("Received response '%.*s' from ", datalen, (char *) data);
  LOG_INFO_6ADDR(sender_addr);
#if LLSEC802154_CONF_ENABLED
  LOG_INFO_(" LLSEC LV:%d", uipbuf_get_attr(UIPBUF_ATTR_LLSEC_LEVEL));
#endif
  LOG_INFO_("\n");
  rx_count++;
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(udp_client_process, ev, data)
{
  static struct etimer periodic_timer;
  static char str[64];
  uip_ipaddr_t dest_ipaddr;
  static uint32_t tx_count;
  static uint32_t missed_tx_count;

  PROCESS_BEGIN();

  /* Initialize UDP connection */
  simple_udp_register(&udp_conn, UDP_CLIENT_PORT, NULL,
                      UDP_SERVER_PORT, udp_rx_callback);

  etimer_set(&periodic_timer, random_rand() % SEND_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));

    if(NETSTACK_ROUTING.node_is_reachable() &&
        NETSTACK_ROUTING.get_root_ipaddr(&dest_ipaddr)) {

      /* Print statistics every 10th TX */
      if(tx_count % 10 == 0) {
        LOG_INFO("Tx/Rx/MissedTx: %" PRIu32 "/%" PRIu32 "/%" PRIu32 "\n",
                 tx_count, rx_count, missed_tx_count);
      }

      /* Send to DAG root */
      log_rpl_parent();
      LOG_INFO("Sending request %"PRIu32" to ", tx_count);
      LOG_INFO_6ADDR(&dest_ipaddr);
      LOG_INFO_("\n");
      snprintf(str, sizeof(str), "BIN seq=%" PRIu32 " fill=%u",
               tx_count, simulated_fill());
      LOG_INFO("BIN_TX %s bytes=%u\n", str, (unsigned)strlen(str));
      simple_udp_sendto(&udp_conn, str, strlen(str), &dest_ipaddr);
      tx_count++;
    } else {
      LOG_INFO("Not reachable yet\n");
      if(tx_count > 0) {
        missed_tx_count++;
      }
    }

    /* Add some jitter */
    #if ADAPTIVE_REPORTING
    etimer_set(&periodic_timer,
      (simulated_fill() >= 80 ? 2 :
       simulated_fill() >= 60 ? 5 : 15) * CLOCK_SECOND
      - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
#else
    etimer_set(&periodic_timer, SEND_INTERVAL
      - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
#endif
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
